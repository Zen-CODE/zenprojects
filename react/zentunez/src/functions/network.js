/**
 * This module houses various functions for providing specific functionality.
 */

const MAX_QUEUE_LENGTH = 5;
var queue_length = 0;

 /**
  * Perform a fetch on the specified URL. If the last call has not returned, ignore the
  * fetch
  *
  * @param {String} url - the URL to fetch
  * @param {Function} callback - the function to call when the fetch is complete (if specified)
  *                              This function should accept a single parameter: the
  *                              JSON-ized response.,
  * @param {Boolean} force - If true, the queue will be reset and the message forced through.
  *                          This is intended to be used with manual interactions, to reset
  *                          the quueue when it blocks
  */
export function queued_fetch(url, callback=null, force=false ){
    if (force) { queue_length = 0};
    if (queue_length < MAX_QUEUE_LENGTH) {
        console.log("Queue ready. Making request...");
        queue_length += 1;
        fetch(url)
            .then(res => res.json())
            .then((response) => {
                queue_length -= 1;
                if (callback !== null){ callback(response) }
            }
        )
    } else {
        console.log("Ignoring queue request");
    }
}
