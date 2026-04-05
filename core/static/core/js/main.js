const chatbotBox = document.getElementById('chatbotBox');
const chatbotToggle = document.getElementById('chatbotToggle');
const chatbotClose = document.getElementById('chatbotClose');
const chatForm = document.getElementById('chatForm');
const chatInput = document.getElementById('chatInput');
const chatMessages = document.getElementById('chatMessages');

function getSessionId() {
  let sessionId = localStorage.getItem('roofmate_chat_session_id');
  if (!sessionId) {
    sessionId = 'session_' + Math.random().toString(36).slice(2) + Date.now();
    localStorage.setItem('roofmate_chat_session_id', sessionId);
  }
  return sessionId;
}

function appendMessage(message, className) {
  if (!chatMessages) return;
  const div = document.createElement('div');
  div.className = className;
  div.textContent = message;
  chatMessages.appendChild(div);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

if (chatbotToggle && chatbotBox) {
  chatbotToggle.addEventListener('click', () => chatbotBox.classList.toggle('active'));
}

if (chatbotClose && chatbotBox) {
  chatbotClose.addEventListener('click', () => chatbotBox.classList.remove('active'));
}

if (chatForm && chatInput) {
  chatForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const message = chatInput.value.trim();
    if (!message) return;

    appendMessage(message, 'user-message');
    chatInput.value = '';

    const csrfInput = chatForm.querySelector('input[name="csrfmiddlewaretoken"]');
    const csrfToken = csrfInput ? csrfInput.value : '';

    try {
      const response = await fetch('/chatbot/reply/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({
          message,
          session_id: getSessionId(),
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        appendMessage(data.error || 'Sorry, something went wrong.', 'bot-message');
        return;
      }

      appendMessage(data.reply || 'Thanks for your message.', 'bot-message');
    } catch (error) {
      appendMessage('Sorry, something went wrong. Please use the enquiry form instead.', 'bot-message');
    }
  });
}
document.addEventListener('DOMContentLoaded', function () {
    const filterButtons = document.querySelectorAll('.filter-btn');
    const galleryCards = document.querySelectorAll('.gallery-card');

    if (filterButtons.length && galleryCards.length) {
        filterButtons.forEach(button => {
            button.addEventListener('click', function () {
                const filter = this.getAttribute('data-filter');

                filterButtons.forEach(btn => btn.classList.remove('active'));
                this.classList.add('active');

                galleryCards.forEach(card => {
                    const category = (card.getAttribute('data-category') || '').toLowerCase();

                    if (filter === 'all' || category.includes(filter)) {
                        card.classList.remove('hide');
                    } else {
                        card.classList.add('hide');
                    }
                });
            });
        });
    }

    const modal = document.getElementById('galleryModal');
    const modalImage = document.getElementById('galleryModalImage');
    const modalCaption = document.getElementById('galleryModalCaption');
    const modalClose = document.getElementById('galleryModalClose');

    if (modal && modalImage && modalCaption && modalClose && galleryCards.length) {
        galleryCards.forEach(card => {
            card.addEventListener('click', function () {
                const image = this.getAttribute('data-image');
                const title = this.getAttribute('data-title');

                modalImage.src = image;
                modalImage.alt = title;
                modalCaption.textContent = title;
                modal.classList.add('active');
                document.body.style.overflow = 'hidden';
            });
        });

        modalClose.addEventListener('click', function () {
            modal.classList.remove('active');
            document.body.style.overflow = '';
        });

        modal.addEventListener('click', function (e) {
            if (e.target === modal) {
                modal.classList.remove('active');
                document.body.style.overflow = '';
            }
        });

        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape') {
                modal.classList.remove('active');
                document.body.style.overflow = '';
            }
        });
    }

    const sliders = document.querySelectorAll('.ba-card');

    if (sliders.length) {
        sliders.forEach(card => {
            const range = card.querySelector('.ba-range');
            const beforeWrap = card.querySelector('.ba-before-wrap');
            const divider = card.querySelector('.ba-divider');

            if (!range || !beforeWrap || !divider) return;

            const updateSlider = (value) => {
                beforeWrap.style.width = value + '%';
                divider.style.left = value + '%';
            };

            updateSlider(range.value);

            range.addEventListener('input', function () {
                updateSlider(this.value);
            });
        });
    }
});