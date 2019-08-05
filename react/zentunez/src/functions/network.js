/**
 * This module houses various functions for providing specific functionality.
 */

var queue_ready = true;

 /**
  * Perform a fetch on the specified URL. If the last call has not returned, ignore the
  * fetch
  *
  * @param {String} url - the URL to fetch
  * @param {Function} callback - the function to call when the fetch is complete.
  *                              This function should accept a single parameter: the
  *                              JSON-ized response
  */
export function queued_fetch(url, callback ){
    if (queue_ready) {
        console.log("Queue ready. Making request...");
        queue_ready = false;
        fetch(url)
            .then(res => res.json())
            .then((response) => {
                callback(response);
                queue_ready = true;
            }
        )
    } else {
        console.log("Ignoring queue request");
    }
}
