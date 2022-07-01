
window.onload = (() => {
    var wrapper = document.getElementById("Button_wrapper")
    // number of questions
    for (let index = 1; index < Number(sessionStorage.getItem('number')) + 1; index++) {
        const element = createAnswer(index)
        wrapper.append(element)
    }
})

function createAnswer(_index) {
    var element = document.createElement("button")
    element.classList.add("Answer_button", "col-4", "btn", "py-4", "px-2", "mb-2", "text-white",
        "col-md-12", "col-lg-5", "position-relative")
    if (_index % 2 === 1) {
        element.classList.add("me-lg-2")
    }
    element.textContent = "Answer " + _index
    switch (_index) {
        case 1:
            element.style.backgroundColor = "#F83962"
            break

        case 2:
            element.style.backgroundColor = "#2EBFD5"
            break

        case 3:
            element.style.backgroundColor = "#FF943B"
            break

        case 4:
            element.style.backgroundColor = "#467CD3"
            break

        case 5:
            element.style.backgroundColor = "#8AC600"
            break

        case 6:
            element.style.backgroundColor = "#9D3FE1"
            break
    }
    // type of question
    if (sessionStorage.getItem("type") != "Interview") {
        addEvent(element, sessionStorage.getItem("type"))
        var badge = document.createElement('button')
        console.log(sessionStorage.getItem("type"))
        switch (sessionStorage.getItem("type")) {
            case "Single answer":
                badge.classList.add('Badge', 'position-absolute', 'top-0', 'end-0', 'translate-middle-y', 'p-2', 'mt-3', 'me-2', 'border', 'border-light', 'rounded-circle', 'border-5')
                break
            case "Multiple answer":
                badge.classList.add('Badge', 'position-absolute', 'top-0', 'end-0', 'translate-middle-y', 'p-2', 'mt-3', 'me-2', 'border', 'border-light', 'rounded-2', 'border-5')
                break
        }
        badge.style.color = 'white'
        element.append(badge)
    }
    return element
}

var ifSelected = false
var selectedAnswer

function addEvent(_element, type) {
    // type of question
    switch (type) {
        case "Single answer":
            _element.addEventListener('click', () => {
                if (ifSelected === true) {
                    selectedAnswer.lastChild.classList.toggle('bg-dark')
                    _element.lastChild.classList.toggle('bg-dark')
                }
                else {
                    _element.lastChild.classList.toggle('bg-dark')
                }
                selectedAnswer = _element
                ifSelected = true
            })
            break
        case "Multiple answer":
            _element.addEventListener('click', () => {
                _element.lastChild.classList.toggle('bg-dark')
            })
            break
    }
}