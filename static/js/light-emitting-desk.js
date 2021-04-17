let switchOff = function () {
    $.ajax({
        url: '/desk/off',
        type: "POST",
        contentType: 'application/json'
    })

    colourPicker.color.rgb = {
        r: 0,
        g: 0,
        b: 0
    }

    setBG([0, 0, 0])
    colourButtons([0, 0, 0])
}

let setColour = function (colour) {
    postColourChange(colourObjectAsArray(colour))
    setBG(colourObjectAsArray(colour))
    colourButtons(colourObjectAsArray(colour))

    if (["sweep", "caterpillar"].includes(loadMode())) {
        flipDirection()
    }
}

let colourObjectAsArray = function (colour) {
    return [colour.red, colour.green, colour.blue]
}

let setBG = function (colour) {
    $('body').css('background-color', colourAsRGB(colour))

    backgroundImageSuffix = 'dark'
    if (isDark(colour)) {
        backgroundImageSuffix = 'light'
    }
    $('body').css('background-image', `url("/static/images/checkboard-${backgroundImageSuffix}.png")`)
}

let colourButtons = function (colour) {
    $('.button').css('background-color', colourAsRGB(colour))

    altColour = 'black'
    if (isDark(colour)) {
        altColour = 'white'
    }

    $('.button').css('border-color', altColour)
    $('.button').css('color', altColour)
}

let colourAsRGB = function (colour) {
    return `rgb(${colour[0]}, ${colour[1]}, ${colour[2]})`
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
        saveMode(defaultMode)
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

let toggleModal = function () {
    if ($('#mode-modal').hasClass('is-active')) {
        $('#mode-modal').removeClass('is-active')
    } else {
        $('#mode-modal').addClass('is-active')
    }
}

let invertColour = function (colour) {
    return colour.map(x => 255 - x)
}

// fuckery follows

// https://stackoverflow.com/a/54070620
let rgb2hsv = function (rgb) {
    let r = rgb[0]
    let g = rgb[1]
    let b = rgb[2]

    let v = Math.max(r, g, b), c = v - Math.min(r, g, b)
    let h = c && ((v == r) ? (g - b) / c : ((v == g) ? 2 + (b - r) / c : 4 + (r - g) / c))

    return {
        h: 60 * (h < 0 ? h + 6 : h),
        s: v && c / v,
        v: v / 255
    }
}

// https://github.com/metafizzy/huebee/blob/047bacab3acc8a17bc4d15db74f6b2970dd017be/huebee.js#L481
let isDark = function (colour) {
    var hsv = rgb2hsv(colour)
    let lightness = hsv.v - Math.cos((hsv.h + 70) / 180 * Math.PI) * 0.15

    return lightness < 0.5
}
