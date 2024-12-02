/* eslint-disable jest/valid-expect */
/* eslint-disable jest/no-hooks */
/* eslint-disable no-undef */
/* eslint-disable jest/prefer-todo */
/* eslint-disable jest/prefer-expect-assertions */
/* eslint-disable jest/expect-expect */
import { expect } from 'chai';
import { createQueue } from 'kue';
import createPushNotificationsJobs from './8-job';

describe('createPushNotificationsJobs', () => {
  const queue = createQueue();

  before(() => {
    queue.testMode.enter();
  });
  after(() => {
    queue.testMode.exit();
  });
  afterEach(() => {
    queue.testMode.clear();
  });

  it('display an error message if jobs is not an array', () => {
    expect(() => {
      createPushNotificationsJobs('not an array', queue);
    }).to.throw('Jobs is not an array');
  });
  it('adds jobs to the queue with the correct type', () => {
    expect(queue.testMode.jobs.length).to.equal(0);
    const jobInfos = [
      {
        phoneNumber: '44556677889',
        message: 'Use the code 1982 to verify your account',
      },
      {
        phoneNumber: '98877665544',
        message: 'Use the code 1738 to verify your account',
      },
    ];
    createPushNotificationsJobs(jobInfos, queue);
    expect(queue.testMode.jobs.length).to.equal(2);
    expect(queue.testMode.jobs[0].data).to.deep.equal(jobInfos[0]);
    expect(queue.testMode.jobs[0].type).to.equal('push_notification_code_3');
  });
});
