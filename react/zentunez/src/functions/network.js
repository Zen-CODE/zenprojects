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
  * @param {Boolean} force - If true, the queue will be reset and the message forced through.
  *                          This is intended to be used with manual interactions, to reset
  *                          the quueue when it blocks
  */
export function queued_fetch(url, callback, force=false ){
    if (force) { queue_ready = true};
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
