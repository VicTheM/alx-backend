import { createClient } from 'redis';
import { promisify } from 'util';
import express from 'express';

const listProducts = [
  {
    itemId: 1,
    itemName: 'Suitcase 250',
    price: 50,
    initialAvailableQuantity: 4,
  },
  {
    itemId: 2,
    itemName: 'Suitcase 450',
    price: 100,
    initialAvailableQuantity: 10,
  },
  {
    itemId: 3,
    itemName: 'Suitcase 650',
    price: 350,
    initialAvailableQuantity: 2,
  },
  {
    itemId: 4,
    itemName: 'Suitcase 1050',
    price: 550,
    initialAvailableQuantity: 5,
  },
];

const PORT = 1245;
const app = express();
const client = createClient()
  .on('connect', () => {
    console.log('Redis client connected to the server');
  })
  .on('error', (err) => {
    console.log('Redis client not connected to the server:', err.message);
  });

function getItemById(id) {
  return listProducts.find((product) => product.itemId === id);
}

async function reserveStockById(itemId, stock) {
  return promisify(client.set).bind(client)(`item.${itemId}`, stock);
}
async function getCurrentReservedStockById(itemId) {
  return promisify(client.get).bind(client)(`item.${itemId}`);
}

app.get('/list_products', (req, res) => {
  res.json(listProducts);
});

app.get('/list_products/:itemId', (req, res) => {
  let { itemId } = req.params;
  itemId = parseInt(itemId, 10);

  const item = getItemById(itemId);
  if (item) {
    getCurrentReservedStockById(itemId)
      .then((stock) => {
        const reserved = parseInt(stock || 0, 10);
        item.currentQuantity = item.initialAvailableQuantity - reserved;
        res.json(item);
      });
  } else {
    res.status(404).json({ status: 'Product not found' });
  }
});

app.get('/reserve_product/:itemId', (req, res) => {
  let { itemId } = req.params;
  itemId = parseInt(itemId, 10);

  const item = getItemById(itemId);
  if (!item) {
    res.status(404).json({ status: 'Product not found' });
    return;
  }
  getCurrentReservedStockById(itemId)
    .then((stock) => {
      const reserved = parseInt(stock || 0, 10);
      if (reserved < item.initialAvailableQuantity) {
        reserveStockById(itemId, reserved + 1)
          .then(() => {
            res.json({ status: 'Reservation confirmed', itemId });
          });
        return;
      }
      res.json({ status: 'Not enough stock available', itemId });
    });
});

function resetStock() {
  return Promise.all(
    listProducts.map(
      (item) => promisify(client.set).bind(client)(`item.${item.itemId}`, 0),
    ),
  );
}

app.listen(PORT, () => {
  resetStock();
  console.log(`Server listening on port ${PORT}`);
});
