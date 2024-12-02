import { createClient } from 'redis';
import { createQueue } from 'kue';
import { promisify } from 'util';
import express from 'express';

const PORT = 1245;
const app = express();
const client = createClient()
  .on('connect', () => {
    console.log('Redis client connected to the server');
  })
  .on('error', (err) => {
    console.log('Redis client not connected to the server:', err.message);
  });
let reservationEnabled = true;
const queue = createQueue();
const initialSeatsCount = 50;

async function reserveSeat(number) {
  return promisify(client.set).bind(client)('available_seats', number);
}

async function getCurrentAvailableSeats() {
  return promisify(client.get).bind(client)('available_seats');
}

app.get('/available_seats', (req, res) => {
  getCurrentAvailableSeats()
    .then((numberOfAvailableSeats) => {
      res.json({ numberOfAvailableSeats });
    });
});

app.get('/reserve_seat', (req, res) => {
  if (!reservationEnabled) {
    res.json({ status: 'Reservation are blocked' });
    return;
  }
  try {
    const job = queue.create('reserve_seat');
    job
      .on('enqueue', () => {
        res.json({ status: 'Reservation in process' });
      })
      .on('complete', () => {
        console.log(`Seat reservation job ${job.id} completed`);
      })
      .on('failed', (err) => {
        console.log(`Seat reservation job ${job.id} failed: ${err.toString()}`);
      });
    job.save();
  } catch (err) {
    res.json({ status: 'Reservation failed' });
  }
});

app.get('/process', (req, res) => {
  res.json({ status: 'Queue processing' });
  queue.process('reserve_seat', (job, done) => {
    getCurrentAvailableSeats()
      .then((numberOfAvailableSeats) => {
        const newNumberOfAvailableSeats = numberOfAvailableSeats - 1;
        console.log(newNumberOfAvailableSeats);
        if (newNumberOfAvailableSeats === 0) {
          reservationEnabled = false;
        }

        if (newNumberOfAvailableSeats >= 0) {
          reserveSeat(newNumberOfAvailableSeats)
            .then(() => done());
        } else {
          done(Error('Not enough seats available'));
        }
      });
  });
});

app.listen(PORT, () => {
  reserveSeat(initialSeatsCount);
  console.log(`Server listening on port ${PORT}`);
});
