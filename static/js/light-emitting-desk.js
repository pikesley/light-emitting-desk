let isBlack = function (colour) {
    return colour[0] == 0 && colour[1] == 0 && colour[2] == 0
}

let switchOff = function () {
    setColour(
        {
            red: 0,
            green: 0,
            blue: 0
        }
    )
}

let setColour = function (colour) {
    postColourChange([colour.red, colour.green, colour.blue])

    if (["sweep", "caterpillar"].includes(loadMode())) {
        flipDirection()
    }
}

let postColourChange = function (colour) {
    $.ajax({
        url: '/desk/light',
        type: "POST",
        contentType: 'application/json',
        data: JSON.stringify(
            {
                'colour': colour,
                'direction': loadDirection(),
                'mode': loadMode(),
                'delay': 0.01
            }
        )
    })
}

let loadDirection = function () {
    if (!window.localStorage['direction']) {
        saveDirection('forwards')
    }
    return window.localStorage['direction']
}

let saveDirection = function (direction) {
    window.localStorage['direction'] = direction
}

let flipDirection = function () {
    if (loadDirection() == 'forwards') {
        saveDirection('backwards')
    } else {
        saveDirection('forwards')
    }
}

let saveMode = function (mode) {
    window.localStorage['mode'] = mode
}

let loadMode = function () {
    if (!window.localStorage['mode']) {
        saveMode('diverge')
    }
    return window.localStorage['mode']
}

let setMode = function (mode) {
    saveMode(mode)
    $('#mode-picker').children().each(function (i, elem) {
        $(elem).removeClass("active")
    })
    $(`#${mode}-select`).addClass("active")
}
