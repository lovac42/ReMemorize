# ReMemorize
Anki Addon: Rescheduler with sibling and logging

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
- Unlike other reschedulers, this addon will not tamper with the ease factor on rescheduling as it avoids the anki api.

### Bug/feature:
Undoing reschedules will include siblings as well if sibling rescheduling was turned on.

