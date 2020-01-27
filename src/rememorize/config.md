# ReMemorize: Rescheduler with sibling and logging

NOTE: Changing config settings do not require a restart unless restart was specified in the notes.

### hotkey:
Shortcut for rememorize.  
(Beware of hotkey conflicts.)

### ef_hotkey:
Shortcut for changing ease factor.  
(Beware of hotkey conflicts.)

### fg_hotkey:
Shortcut for forget note.  
(Beware of hotkey conflicts.)

### default_days_on_ask
Default days to set when the user presses the hotkey.

### revlog_rescheduled:
Turn on Logging?

### change_due_grad_new_card:
Defaults to true, this graduates new cards when rescheduling due (negative numbers). If you want to keep all the learning steps, then set this to false.

### fuzz_days:
Fuzz interval and due date? true or false  
Used by positive integer input during review or reschedule option in browser.  
Uses Anki's native fuzz api and works with load balancer or free weekend on V1 & V2.

### fuzz_dues:
Fuzz the due date? true or false  
Used by negative integer input during reviews.  
Uses Anki's native fuzz api and works with load balancer or free weekend on V2 only.

### bury_siblings:
Bury sibling cards due today if the current card has been rescheduled.

### forget_siblings:
(On ForgetCard) Make siblings into new cards as well?  
(This will not affect the browser.)  
Useful for flipping through unspended old material.  
Do not forget to turn this back off.  

### reschedule_sibling:
(On RescheduleCard) Reschedule siblings as well?  
(This will not affect the browser.)  
Useful for going through imported shared decks with alot of siblings.  
Do not forget to turn this back off.  

### reschedule_siblings_on_again:
Checks sibling boundary whenever the "Again" button was pressed. e.g. The front is due tomorrow as a leech card with an IVL of 1 and the reverse card is due in 9 month from now with an IVL of 450.

### sibling_boundary:
Sets the limit, reschedule if sibling IVL exceeds this limit.

### sibling_fuzz_min, sibling_fuzz_max
fuzz days. Set to the same value to avoid fuzz.

### automatic_mode:
Don't ask user, just reschedule all out-of-bound siblings.

### replace_brower_reschedule:
Replaces the card browser's function for reschedCards with rememorize functions.  
Use "Reschedule..." to change the due/ivl of the card.  

### replace_brower_reposition:
Replaces the card browser's function for reposition with rememorize functions.  
Use "Reposition..." to change the due only. (Same as using negative numbers during review.)  
For new cards, Ivl will be set to the graduating interval set in deck options, unless "skip_new_card_types_on_reposition" is set to true.  
New/new-lrn card changes are logged, if revlog_rescheduled is enabled. Since the intervals do not change on review cards, they will not be logged.  

### skip_new_card_types_on_reposition:
If enabled, on new cards, it will invoke the old browser reposition method to change the card's position instead of rescheduling the due date.  
New cards take priority, you can't mix review and new types.  

