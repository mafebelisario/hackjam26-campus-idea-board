// Workshop Step 1: connect the HTML form to our Flask API.
const form = document.querySelector('#idea-form');
const list = document.querySelector('#ideas');
const filter = document.querySelector('#filter');
const message = document.querySelector('#message');
let allIdeas = [];

function renderIdeas() {
  const selected = filter.value;
  const visible = allIdeas.filter(idea => selected === 'All' || idea.category === selected);
  document.querySelector('#count').textContent = `${allIdeas.length} ideas`;
  list.replaceChildren(); // Safe DOM rendering: never inject user text as HTML.
  if (!visible.length) {
    const empty = document.createElement('p');
    empty.className = 'muted';
    empty.textContent = 'No ideas yet for this track. Be the first!';
    list.append(empty);
    return;
  }
  visible.forEach(idea => {
    const card = document.createElement('article'); card.className = 'idea';
    const pill = document.createElement('span'); pill.className = 'pill'; pill.textContent = idea.category;
    const title = document.createElement('h3'); title.textContent = idea.title;
    const description = document.createElement('p'); description.textContent = idea.description;
    const bottom = document.createElement('div'); bottom.className = 'idea-bottom';
    const date = document.createElement('small'); date.textContent = `Idea #${idea.id}`;
    const vote = document.createElement('button'); vote.className = 'vote';
    vote.textContent = `▲ ${idea.votes} votes`;
    vote.addEventListener('click', async () => {
      try {
        const response = await fetch(`/api/ideas/${idea.id}/upvote`, {method:'POST'});
        if (!response.ok) throw new Error('Could not vote');
        await loadIdeas();
      } catch (error) { message.textContent = error.message; }
    });
    bottom.append(date, vote); card.append(pill, title, description, bottom); list.append(card);
  });
}

async function loadIdeas() {
  const response = await fetch('/api/ideas');
  if (!response.ok) throw new Error('Could not load ideas. Is Flask running?');
  allIdeas = await response.json();
  renderIdeas();
}

form.addEventListener('submit', async event => {
  event.preventDefault();
  const idea = {
    title: document.querySelector('#title').value.trim(),
    description: document.querySelector('#description').value.trim(),
    category: document.querySelector('#category').value
  };
  message.textContent = 'Submitting...';
  try {
    const response = await fetch('/api/ideas', {
      method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(idea)
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || 'Submission failed');
    form.reset(); message.textContent = '✓ Idea added!';
    await loadIdeas();
  } catch (error) { message.textContent = error.message; }
});
filter.addEventListener('change', renderIdeas);
loadIdeas().catch(error => {list.textContent = error.message;});
