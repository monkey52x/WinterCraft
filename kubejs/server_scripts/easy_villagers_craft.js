ServerEvents.recipes(event => {
  // Вы добавляете свой код рецепта СЮДА, внутри фигурных скобок колбэка.
  event.shaped(
    Item.of('easy_villagers:villager', 1), // arg 1: output
    [
      ' A ',
      ' B ', // arg 2: the shape (array of strings)
      '   '
    ],
    {
      A: 'easy_villagers:trader',
      B: 'minecraft:nether_star'
    }
  )

  // Этот вызов console.log уже был в вашем исходном примере,
  // он просто остается внутри того же слушателя событий.
  console.log('Hello! The recipe event has fired!')
})