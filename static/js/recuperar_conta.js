document.addEventListener("DOMContentLoaded", function () {
    const cardHTML = `
        <div class="card-login">
            <div class="titulo">
                <p>Recuperação de Conta</p>
            </div>
            <form action="">
                <div class="inputs">
                    <div class="input-login">
                        <label for="email">E-mail</label>
                        <input id="email" placeholder="Digite seu e-mail" type="email">
                    </div>
                </div>
                <div class="button-div">
                    <button id="enviar-codigo">Enviar Código</button>
                </div>
            </form>
        </div>
    `;

    document.getElementById("card").innerHTML = cardHTML;

    document.getElementById("enviar-codigo").addEventListener("click", function (event) {
        event.preventDefault();
        const email = document.getElementById("email").value;
        if (email) {
            console.log("Código de recuperação enviado para:", email);
            card_enviar_codigo();
        } else {
            console.log("Por favor, insira um e-mail válido.");
        }
    });
});

function card_enviar_codigo() {
    const card = `
        <div class="card-login">
            <div class="titulo">
                <p>Insira o Código</p>
            </div>
            <form action="">
                <div class="codigo-container">
                    ${'<input type="text" maxlength="1" class="codigo" required>'.repeat(6)}
                </div>
                <div class="button-div">
                    <button type="submit" id="verificar-codigo">Verificar Código</button>
                </div>
            </form>
        </div>
    `;

    document.getElementById("card").innerHTML = card;

    const inputs = document.querySelectorAll(".codigo");

    inputs.forEach((input, index) => {
        input.addEventListener("input", () => {
            if (input.value.length === 1 && index < inputs.length - 1) {
                inputs[index + 1].focus();
            }
        });

        input.addEventListener("keydown", (e) => {
            if (e.key === "Backspace" && input.value === "" && index > 0) {
                inputs[index - 1].focus();
            }
        });
    });
}
