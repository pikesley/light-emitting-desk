describe("loadDirection", function () {
  it("loads the default direction", function () {
    window.localStorage.clear()
    expect(loadDirection()).toEqual('forwards')
  })
})

describe("saveDirection", function () {
  it("saves the direction", function () {
    saveDirection('backwards')
    expect(loadDirection()).toEqual('backwards')
  })
})

describe("flipDirection", function () {
  it("flips the direction", function () {
    saveDirection('forwards')
    expect(loadDirection()).toEqual('forwards')

    flipDirection()
    expect(loadDirection()).toEqual('backwards')

    flipDirection()
    flipDirection()
    expect(loadDirection()).toEqual('backwards')
  })
})

describe("loadMode", function () {
  it("loads the mode", function () {
    defaultMode = "some-mode"
    window.localStorage.clear()
    expect(loadMode()).toEqual('some-mode')
  })
})

describe("saveMode", function () {
  it("saves the mode", function () {
    saveMode('sweep')
    expect(loadMode()).toEqual('sweep')
  })
})

describe("setColour", function () {
  it("sets a colour", function () {
    postColourChange = jasmine.createSpy().and.callFake(postColourChange)
    flipDirection = jasmine.createSpy().and.callFake(flipDirection)

    saveMode('sweep')
    setColour({ red: 1, green: 2, blue: 3 })

    expect(postColourChange).toHaveBeenCalledWith([1, 2, 3])
    expect(flipDirection).toHaveBeenCalled()
  })
})

describe("invertColour", function () {
  it("inverts a colour", function () {
    expect(invertColour([255, 255, 255])).toEqual([0, 0, 0])
    expect(invertColour([0, 0, 0])).toEqual([255, 255, 255])
    expect(invertColour([19, 102, 200])).toEqual([236, 153, 55])
  })
})

describe("isDark", function () {
  it("knows if a colour is dark", function () {
    expect(isDark([0, 0, 0])).toBe(true)
    expect(isDark([255, 255, 255])).toBe(false)
    expect(isDark([255, 0, 255])).toBe(false)
    expect(isDark([0, 0, 127])).toBe(true)
  })
})
