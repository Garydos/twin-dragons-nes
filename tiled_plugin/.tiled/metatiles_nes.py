from tiled import *

#Which palette does each metatile use? Edit this to the appropriate palette
#number when making new metatiles (metatile_number : palette_number)
tile_attrs = {
    0:0,
    1:1,
    2:2,
    3:2,
    4:2,
    5:2,
    6:1,
    7:2,
    8:1,
    9:1,
    10:2,
    11:1,
    12:1,
    13:1,
    14:1,
    15:1,
    16:1,
    17:2,
    18:1,
    19:2,
    20:2,
    21:2,
    22:1,
    255:1
}

def rle_compress(arr: list, column_width: int):
    if len(arr) == 0:
        return []

    compressed_arr = []
    #split the array into multiple arrays of length column_width
    column_split_arr = [arr[i:i+column_width] for i in range(0, len(arr), column_width)]
    
    for column in column_split_arr:
        counter = 1
        prev_item = column[0]
        for item in column[1:]:
            if item == prev_item:
                counter += 1
            else:
                compressed_arr.append(counter)
                compressed_arr.append(prev_item)
                counter = 1
                prev_item = item
        compressed_arr.append(counter)
        compressed_arr.append(prev_item)
        
    return compressed_arr

def set_attr(tile_num : int, meta_row : int, meta_col : int, attrs_arr : list):
    attr_row = (meta_row//2)
    attr_col = (meta_col//2)
    attr_index = (attr_col * 8) + attr_row
    
    attributes = tile_attrs[tile_num]
    
    if meta_row % 2 == 0 and meta_col % 2 == 0:
        attributes <<= 0
    elif meta_row % 2 == 0 and meta_col % 2 == 1:
        attributes <<= 2
    elif meta_row % 2 == 1 and meta_col % 2 == 0:
        attributes <<= 4
    else:
        attributes <<= 6

    attrs_arr[attr_index] |= attributes

class Example(Plugin):
    @classmethod
    def nameFilter(cls):
        return "Metatile files (*.meta)"

    @classmethod
    def shortName(cls):
        return "metatiles"

    @classmethod
    def write(cls, tileMap, fileName):
        attrs = [0 for i in range(8 * (tileMap.width() // 2))]
        metatiles = []
        #Metatiles
        for i in range(tileMap.layerCount()):
            if isTileLayerAt(tileMap, i) and tileLayerAt(tileMap, i).name() == "Tiles":
                tileLayer = tileLayerAt(tileMap, i)
                for x in range(tileLayer.width()):
                    for y in range(tileLayer.height()):
                        set_attr(tileLayer.cellAt(x, y).tile().id(), y, x, attrs)
                        metatiles.append(tileLayer.cellAt(x, y).tile().id())
                    metatiles.append(255)
        metatiles = rle_compress(metatiles,16)
        with open(fileName, 'wb') as fileHandle:
            fileHandle.write(bytes(metatiles))
        #Metatiles Size
        with open(fileName.rsplit(".",maxsplit=1)[0] + ".meta_size", 'wb') as fileHandle:
            fileHandle.write(len(metatiles).to_bytes(2, byteorder='little'))
        #Attributes
        attrs = rle_compress(attrs,8)
        with open(fileName.rsplit(".",maxsplit=1)[0] + ".attrs", 'wb') as fileHandle:
            fileHandle.write(bytes(attrs))
        #Attributes Size
        with open(fileName.rsplit(".",maxsplit=1)[0] + ".attrs_size", 'wb') as fileHandle:
            fileHandle.write(len(attrs).to_bytes(2, byteorder='little'))
        #Enemy Spawns
        enemies = []
        enemy_spawn_columns = []
        enemy_info = []
        for i in range(tileMap.layerCount()):
            if isObjectGroupAt(tileMap, i) and tileLayerAt(tileMap, i).name() == "Enemies":
                objectGroup = objectGroupAt(tileMap, i)
                for j in range(objectGroup.objectCount()):
                    enemies.append(objectGroup.objectAt(j))
        enemies.sort(key=lambda enemy: enemy.x()) #sort by x position
        for enemy in enemies:
            enemy_spawn_columns.append(int(enemy.x()) // 8)
            enemy_type = int(enemy.propertyAsString('enemy_type'))
            y_spawn_location = int(enemy.y())
            enemy_info.append((enemy_type << 8) + y_spawn_location)
        #Enemy spawn column numbers
        with open(fileName.rsplit(".",maxsplit=1)[0] + ".enemies", 'wb') as fileHandle:    
            for col in enemy_spawn_columns:
                fileHandle.write(col.to_bytes(2, byteorder='little'))
        #Enemy spawn info bytes
        with open(fileName.rsplit(".",maxsplit=1)[0] + ".enemies_info", 'wb') as fileHandle:    
            for byte in enemy_info:
                fileHandle.write(byte.to_bytes(2, byteorder='little'))
        #Max screen number (number of screens - 1)
        with open(fileName.rsplit(".",maxsplit=1)[0] + ".max_screen", 'wb') as fileHandle:    
            fileHandle.write(((tileMap.width() // 16) - 1).to_bytes(1, byteorder='little'))
        #Number of enemy spawns
        with open(fileName.rsplit(".",maxsplit=1)[0] + ".enemy_spawn_num", 'wb') as fileHandle:    
            fileHandle.write((len(enemy_spawn_columns)).to_bytes(1, byteorder='little'))
        return True