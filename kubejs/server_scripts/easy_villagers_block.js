BlockEvents.rightClicked(event => {
    // Предмет, на который накладываем ограничение
    const BANNED_ITEMS = [
        'easy_villagers:villager'
    ]

    // Белый список блоков (только на них можно нажимать этим предметом)
    const ALLOWED_BLOCKS = [
        'easy_villagers:trader', 
        'easy_villagers:auto_trader', 
        'easy_villagers:farmer', 
        'easy_villagers:breeder', 
        'easy_villagers:converter', 
        'easy_villagers:iron_farm', 
        'easy_villagers:incubator'
    ]

    let player = event.player
    let heldItemId = event.item.id
    let targetBlockId = event.block.id

    // Если игрок держит запрещенный предмет
    if (BANNED_ITEMS.includes(heldItemId)) {
        
        // ПРОВЕРКА: Если блок НЕ в белом списке ИЛИ если игрок зажал Shift
        // Это заблокирует попытку поставить жителя на землю через Shift+ПКМ
        if (!ALLOWED_BLOCKS.includes(targetBlockId) || player.isCrouching()) {
            
            // Если игрок нажимает Shift на разрешенном блоке, мы все равно можем захотеть это запретить,
            // так как Shift обычно заставляет игрока ставить предмет РЯДОМ или НА блок, а не В него.
            player.tell('§cЭтого жителя можно поместить только внутрь блоков Easy Villagers!')
            event.cancel()
        }
    }
})