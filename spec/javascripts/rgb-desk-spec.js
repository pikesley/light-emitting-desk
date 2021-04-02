describe("isBlack", function () {
  it("knows when a colour is black", function () {
    expect(isBlack([0, 0, 0])).toBe(true)
  })

  it("knows when a colour is not black", function () {
    expect(isBlack([0, 255, 0])).toBe(false)
  })
})

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
    window.localStorage.clear()
    expect(loadMode()).toEqual('diverge')
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

describe("switchOff", function () {
  it("turns off the lights", function () {
    saveDirection('backwards')
    setColour = jasmine.createSpy().and.callFake(setColour);

    switchOff()

    expect(setColour).toHaveBeenCalledWith({ red: 0, green: 0, blue: 0 })
  })
})
