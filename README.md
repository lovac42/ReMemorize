# ReMemorize: Rescheduler with sibling and logging

https://ankiweb.net/shared/info/323586997  

<i>"It is recommended that you always re-memorize items whose content has changed significantly ... Re-memorize items of high priority that have changed or which are extremely important to your knowledge at a given moment."</i> --<b>Excerpt from the SM 20 Rules.</b>

## About:
This addon allow users to manually adjust properties of the current card in the reviewer. It is meant for advanced users who seek to fine tune certain values. Beginners should avoid tampering with the card values and go read the friendly manual, incrementally or normally.

### Input options:
Enter zero to reset the card as new.  
Positive integer to reschedule the card's ivl and due date.  
Negative integer to reschedule the due date only. Keeping the current IVL.  
You may enter specific dates such as 1/20 or 1/25/2019, this will change the interval and due date (with fuzz). Similar to negative integers, use negative prefix to change the due date only. -1/20, -1/25, etc...  
ReMemorize operates on the current card in the reviewer by default. The "p" prefix (lowercase) will operate on the previous card. p7, p-25, p-1/23, etc...  

p - previous card  
\- (dash) - change due only  
m/d - month/date  
m/d/y - month/date/year  
n - interval and due to n days  


\-3 - change due to 3 days  
p5 - change interval and due of previous card to 5  
p-5/15 - change due of previous card to May 15th  


<img src="https://raw.githubusercontent.com/lovac42/ReMemorize/master/screenshots/gettext.png" />  

### Features include:
- Forget card, makes the card new again.
- Adjust ease factor, changes the difficulty of the card.
- Reschedule changes the interval and due date. Entering 0 forgets the card, and entering a negative value alters the due date only.
- Reschedule siblings of forgotten cards.
- Logging for reschedules
- Undo reschedules
- Unlike other reschedulers, this addon will not reset the ease factor on rescheduling as it avoids the anki api.
- Compatible with addon:noFuzzWhatsoever
- Compatible with addon:FreeWeekend or loadBalancer

### Browser Support:
You can turn on the browser features in config options and have ReMemorize replace Anki's rescheduling methods.

<img src="https://raw.githubusercontent.com/lovac42/ReMemorize/master/screenshots/config.png" />  


### Configs:
Various configs are included in config options including helpful (or unhelpful) notes.  
Anki 2.0 users will need to use the <a href="https://ankiweb.net/shared/info/2058082580">backported addonManager21</a> to change these values.  



## runHooks:
Addon writers can tap into ReMemorize by using runHooks.  
```
runHook("ReMemorize.forget", card)              #make new
runHook("ReMemorize.reschedule", card, 100)     #reschedule 100 days (due+ivl)
runHook("ReMemorize.changeDue", card, 100)      #reschedule 100 days (due)
runHook("ReMemorize.forgetAll", cids)           #make new
runHook("ReMemorize.rescheduleAll", cids, 1, 7) #reschedule rand 1-7 (due+ivl)
runHook("ReMemorize.changeDueAll", cids, 1, 1)  #reschedule 1,2,3,4... (due+stepping)
```


## Screenshots:
<img src="https://raw.githubusercontent.com/lovac42/ReMemorize/master/screenshots/studymenu.png" />  
<img src="https://raw.githubusercontent.com/lovac42/ReMemorize/master/screenshots/gettext.png" />  
<img src="https://raw.githubusercontent.com/lovac42/ReMemorize/master/screenshots/input_opt.png" />  
<img src="https://raw.githubusercontent.com/lovac42/ReMemorize/master/screenshots/date_opt.png" />  
<img src="https://raw.githubusercontent.com/lovac42/ReMemorize/master/screenshots/o_opt.png" />  
<img src="https://raw.githubusercontent.com/lovac42/ReMemorize/master/screenshots/neg_opt.png" />  
<img src="https://raw.githubusercontent.com/lovac42/ReMemorize/master/screenshots/pos_opt.png" />  

<img src="https://raw.githubusercontent.com/lovac42/ReMemorize/master/screenshots/reschedule.png" />  
<img src="https://raw.githubusercontent.com/lovac42/ReMemorize/master/screenshots/stats.png" />  
<img src="https://raw.githubusercontent.com/lovac42/ReMemorize/master/screenshots/dueDate.png" />  
<img src="https://raw.githubusercontent.com/lovac42/ReMemorize/master/screenshots/stepDates.png" />  
<img src="https://raw.githubusercontent.com/lovac42/ReMemorize/master/screenshots/randomDates.png" />  
<img src="https://raw.githubusercontent.com/lovac42/ReMemorize/master/screenshots/randStepDates.png" />  


