document.addEventListener('DOMContentLoaded', () => {
  const menuToggle = document.getElementById('menu-toggle');
  const navbar = document.getElementById('navbar');

  menuToggle.addEventListener('click', () => {
    navbar.classList.toggle('show');
  });
});


document.addEventListener("DOMContentLoaded", () => {
  const header = document.querySelector("header");
  let lastScrollTop = 0;

  window.addEventListener("scroll", () => {
    const currentScroll = window.pageYOffset;

    if (currentScroll > lastScrollTop) {
      // Scrolling down
      header.style.transform = "translateY(-100%)";
    } else {
      // Scrolling up
      header.style.transform = "translateY(0)";
    }

    lastScrollTop = currentScroll <= 0 ? 0 : currentScroll; // Evitar valores negativos
  });
});

document.addEventListener("DOMContentLoaded", () => {
  const header = document.querySelector("header");

  // Obtén la altura del header
  const headerHeight = header.offsetHeight;

  // Actualiza la variable CSS --header-height en el :root
  document.documentElement.style.setProperty('--header-height', `${headerHeight}px`);
});


document.addEventListener("DOMContentLoaded", () => {
  const scrollToTopButton = document.getElementById("scroll-to-top");

  // Mostrar u ocultar el botón dependiendo del scroll
  window.addEventListener("scroll", () => {
    if (window.scrollY > 300) {  // Mostrar el botón después de hacer scroll 300px
      scrollToTopButton.classList.add("show");
    } else {
      scrollToTopButton.classList.remove("show");
    }
  });

  // Función para volver arriba al hacer clic
  scrollToTopButton.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
});


// Al enviar el formulario

const newsletterForm = document.getElementById('newsletterForm');
if (newsletterForm) {

  newsletterForm.addEventListener('submit', async function (event) {
    event.preventDefault(); // Prevenir el comportamiento por defecto (recargar página)

    const emailElement = document.getElementById('email')
    const terminosElement = document.getElementById('terminos');
    const consentimientoElement = document.getElementById('consentimiento');
    const responseMessageElement = document.getElementById('responseMessage');
    const checkboxNewsletterTyC = document.getElementById('checkboxNewsletterTyC');
    const checkboxNewsletterPP = document.getElementById('checkboxNewsletterPP');
    const responseTextElement = document.getElementById('responseText');
    const overlay = document.getElementById('loadingOverlay');
    const submitButton = document.getElementById('submitButton');

    // Función para mostrar el mensaje con el tipo adecuado
    function showMessage(message, type) {
      responseTextElement.textContent = message;
      responseMessageElement.className = type === 'success' ? 'success' : 'error';
      responseMessageElement.style.display = 'block';
    }

    submitButton.disabled = true;
    submitButton.style.cursor = 'not-allowed';
    const email = emailElement.value;
    const terminos = terminosElement.checked;
    const consentimiento = consentimientoElement.checked;

    // Validación básica

    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!email || !terminos || !consentimiento || !emailPattern.test(email)) {
      showMessage("Por favor, completa todos los campos.", 'error');
      
      if (!terminos) {
        checkboxNewsletterTyC.className = 'error';
      } else {
        checkboxNewsletterTyC.className = '';
      }
    
      if (!consentimiento) {
        checkboxNewsletterPP.className = 'error';
      } else {
        checkboxNewsletterPP.className = '';
      }
    
      if (!email) {
        emailElement.className = 'error';
      }
      else if (!emailPattern.test(email)) {
        showMessage("Por favor, introduce un correo electrónico válido.", 'error');
        emailElement.value = ''
        emailElement.className = 'error';
      } 
      else {
        emailElement.className = '';
      }
      submitButton.disabled = false;
      submitButton.style.cursor = 'pointer';
      return;
    }
    
    checkboxNewsletterTyC.className = '';
    checkboxNewsletterPP.className = '';
    emailElement.className = '';

    overlay.style.display = 'flex'; // Mostrar el overlay mientras se espera la respuesta

    // Datos a enviar
    const data = {
      email: email,
      fechaRegistro: new Date().toISOString(),
      terminosAceptados: terminos,
      consentimientoNewsletter: consentimiento
    };

    try {
      const response = await fetch('', {
        method: 'POST',
        body: JSON.stringify(data),
        headers: { 'Content-Type': 'application/json' },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json(); // Obtener la respuesta JSON de la API

      if (result.message) {
        showMessage('Te acabo de enviar un correo a ' + result.message, 'success');
        window.location.href = '/registrado.html';
      } else {
        showMessage('Algo no ha ido bien, inténtalo más tarde o escríbeme para que lo arregle.', 'error');
      }

    } catch (error) {
      showMessage('Algo no ha ido bien, inténtalo más tarde o escríbeme para que lo arregle.', 'error');
      console.error(error);
    } finally {
      overlay.style.display = 'none'; // Ocultar el overlay al finalizar
      submitButton.disabled = false;
      submitButton.style.cursor = 'pointer';
      
    }

  });
}

const closeButton = document.getElementById('closeButton');

// Solo agregar el event listener si el elemento existe
if (closeButton) {
  closeButton.addEventListener('click', function () {
    document.getElementById('responseMessage').style.display = 'none';
    document.getElementById('checkboxNewsletterTyC').className = '';
    document.getElementById('checkboxNewsletterPP').className = '';
    document.getElementById('email').className = '';
    
    if (document.getElementById('message')) {
      document.getElementById('message').className = '';
    }
  });
}


// Formulario de contacto
const contactForm = document.getElementById('contactForm');
if (contactForm) {
  contactForm.addEventListener('submit', async function (event) {
    event.preventDefault(); // Prevenir el comportamiento por defecto (recargar página)

    const nameElement = document.getElementById('name');
    const emailElement = document.getElementById('email');
    const subjectElement = document.getElementById('subject');
    const messageElement = document.getElementById('message');
    const terminosElement = document.getElementById('terminos');
    const consentimientoElement = document.getElementById('consentimiento');
    const responseMessageElement = document.getElementById('responseMessage');
    const checkboxNewsletterTyC = document.getElementById('checkboxNewsletterTyC');
    const checkboxNewsletterPP = document.getElementById('checkboxNewsletterPP');
    const responseTextElement = document.getElementById('responseText');
    const overlay = document.getElementById('loadingOverlay');
    const contactSubmitButton = document.getElementById('contactSubmitButton');

    // Función para mostrar el mensaje con el tipo adecuado
    function showMessage(message, type) {
      responseTextElement.textContent = message;
      responseMessageElement.className = type === 'success' ? 'success' : 'error';
      responseMessageElement.style.display = 'block';
    }

    contactSubmitButton.disabled = true;
    contactSubmitButton.style.cursor = 'not-allowed';

    const name = nameElement.value.trim();
    const email = emailElement.value.trim();
    const subject = subjectElement.value.trim();
    const message = messageElement.value.trim();
    const terminos = terminosElement.checked;
    const consentimiento = consentimientoElement.checked;

    // Validación básica
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!email || !message || !terminos || !consentimiento || !emailPattern.test(email)) {
      showMessage("Por favor, completa todos los campos obligatorios.", 'error');

      checkboxNewsletterTyC.className = terminos ? '' : 'error';
      checkboxNewsletterPP.className = consentimiento ? '' : 'error';
      emailElement.className = emailPattern.test(email) ? '' : 'error';
      messageElement.className = message ? '' : 'error';

      if (!emailPattern.test(email)) {
        showMessage("Por favor, introduce un correo electrónico válido.", 'error');
        emailElement.value = '';
      }

      contactSubmitButton.disabled = false;
      contactSubmitButton.style.cursor = 'pointer';
      return;
    }

    checkboxNewsletterTyC.className = '';
    checkboxNewsletterPP.className = '';
    emailElement.className = '';
    messageElement.className = '';

    overlay.style.display = 'flex'; // Mostrar el overlay mientras se espera la respuesta

    // Datos a enviar
    const data = {
      name: name,
      email: email,
      subject: subject,
      message: message,
      fechaMensaje: new Date().toISOString(),
      terminosAceptados: terminos,
      consentimientoNewsletter: consentimiento
    };

    try {
      const response = await fetch('', {
        method: 'POST',
        body: JSON.stringify(data),
        headers: { 'Content-Type': 'application/json' },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json(); // Obtener la respuesta JSON de la API

      if (result.message) {
        showMessage('Tu mensaje ha sido enviado correctamente.', 'success');
        contactForm.reset();
      } else {
        console.log(response.status)
        console.log(response)
        showMessage('Algo no ha ido bien, inténtalo más tarde.', 'error');
      }

    } catch (error) {
      console.log(response.status)
      console.log(response)
      showMessage('Algo no ha ido bien, inténtalo más tarde.', 'error');
      console.error(error);
    } finally {
      overlay.style.display = 'none'; // Ocultar el overlay al finalizar
      contactSubmitButton.disabled = false;
      contactSubmitButton.style.cursor = 'pointer';
    }
  });
}