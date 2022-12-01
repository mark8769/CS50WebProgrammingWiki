## I guess this is not a fair test, since I am supposed to be using markdown anyway right?

### But using html tags and not closing them, causes the page to be all funky since we are escaping the string, and letting our HTML to be outputted directly to the page.

### This is done by using the {{ some_markdown_context  | safe }} inside our generic_entry.html page. Django and Jinja are cool aren't they?

- Back to the matter, lets start this is off with a list, or maybe something else?

- <h1>A</h1>

- <h3> this is a tag in html

- </h3>

- Lets try an anchor tag?

- <a> 

- some random text

- </a>

- Finally lets not close it out

- <p>

hello

world

is my message getting through