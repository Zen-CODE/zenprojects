/*
    This module houses the test for the ZenPlaylist functionality
*/
const supertest = require('supertest')
const app = require('../app.js')
const request = supertest(app)


it('Test the we can fetch the "Now playing" data.', async () => {
    const response = await request.get('/get_playlist')
  
    expect(response.status).toBe(200)
    expect(typeof(response.body)).toBe('object')
  })
  
it('Test the we can fetch the current tracks info.', async () => {
    const response = await request.get('/get_current_info')
  
    expect(response.status).toBe(200)
    expect(typeof(response.body)).toBe('object')
  })
