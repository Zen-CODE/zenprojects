/*
    This module houses the test for the ZenPlaylist functionality
*/
const supertest = require('supertest')
const app = require('../app.js')
const request = supertest(app)


it('Test the we can fetch the "Now playing" data.', async () => {
    const response = await request.get('/now_playing')
  
    expect(response.status).toBe(200)
    expect(typeof(response.body)).toBe('object')
  })
  