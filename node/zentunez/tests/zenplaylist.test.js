/*
    This module houses the test for the ZenPlaylist functionality
*/
const supertest = require('supertest')
const app = require('../app.js')
const request = supertest(app)
const fetchMock = require('jest-fetch-mock')


it('Test the we can fetch the "Now playing" data.', async () => {
    fetchMock.mockResponseOnce(JSON.stringify({'test': 'response'}));
    
    const response = await request.get('/get_playlist')
  
    expect(response.status).toBe(200)
    expect(typeof(response.body)).toBe('object')
    expect(response.body).toBe({'test': 'response'})
  })
  
it('Test the we can fetch the current tracks info.', async () => {
    const response = await request.get('/get_current_info')
  
    expect(response.status).toBe(200)
    expect(typeof(response.body)).toBe('object')
  })
