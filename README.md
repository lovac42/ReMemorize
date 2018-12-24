# ReMemorize: Rescheduler with sibling and logging

https://ankiweb.net/shared/info/323586997  

"It is recommended that you always re-memorize items whose content has changed significantly ... Re-memorize items of high priority that have changed or which are extremely important to your knowledge at a given moment." --Excerpt from the SM 20 Rules.

## About:
This addon allow users to manually adjust properties of the current card in the reviewer. It is meant for advanced users who seek to fine tune certain values. Beginners should avoid tampering with the card values and go read the friendly manual, incrementally or normally.

### Features include:
- Forget card, makes the card new again.
- Adjust ease factor, changes the difficulty of the card.
- Reschedule changes the interval and due date. Entering 0 forgets the card, and entering a negative value alters the due date only.
- Reschedule siblings of forgotten cards.
- Logging for reschedules
- Undo reschedules
- Unlike other reschedulers, this addon will not reset the ease factor on rescheduling as it avoids the anki api.
- Compatible with addon:noFuzzWhatsoever

### Browser features:
You can turn on the browser features in config options and have ReMemorize replace Anki's rescheduling methods.


### Configs:
Various configs are included in config options including helpful (or unhelpful) notes.  
Anki 2.0 users will need to use the <a href="https://ankiweb.net/shared/info/2058082580">backported addonManager21</a> to change these values.  


### Bug/feature:
Undoing reschedules will include siblings as well if sibling rescheduling was turned on.  
Note: The undo feature in Anki only allows one of two types, reviews and checkpoints. Switching types will clear the other. Here we need checkpoints for undoing siblings, but grading reviews will delete the checkpoints. So we opt to pop each card on to the undo stack, but this requires the user to manually undo each card and their sibling. Fixing this will require rewriting the whole undo feature of Anki.

## runHooks:
Addon writers can tap into ReMemorize by using runHooks.  
```
runHook("ReMemorize.forget", card)              #make new
runHook("ReMemorize.reschedule", card, 100)     #reschedule 100 days (due+ivl)
runHook("ReMemorize.changeDue", card, 100)      #reschedule 100 days (due)
runHook("ReMemorize.rescheduleAll", cids, 1, 7) #reschedule rand 1-7 (due+ivl)
```

## Screenshots:
<img src="https://raw.githubusercontent.com/lovac42/ReMemorize/master/screenshots/studymenu.png" />  
<img src="https://raw.githubusercontent.com/lovac42/ReMemorize/master/screenshots/gettext.png" />  
<img src="https://raw.githubusercontent.com/lovac42/ReMemorize/master/screenshots/reschedule.png" />  
<img src="https://raw.githubusercontent.com/lovac42/ReMemorize/master/screenshots/reposition.png" />  
