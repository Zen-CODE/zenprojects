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
    console.log(`body = ${JSON.stringify(response.body)}`)
    expect(response.body).toEqual({'test': 'response'})
  })
