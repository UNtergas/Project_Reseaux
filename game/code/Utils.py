import pygame

from const import TILE_SIZE, MAP_SIZE, FIRE_THRESHOLD, COLLAPSE_THESHOLD


def GenerateGridLayout(x, y, columnNumber, rowNumber, gapX, gapY, sizeX, sizeY):
    initialOffsetX = - (columnNumber - 1) * (gapX+sizeX) / 2
    initialOffsetY = - (rowNumber - 1) * (gapY+sizeY) / 2

    for c in range(columnNumber):
        for r in range(rowNumber):
            yield (x + initialOffsetX + c*(gapX+sizeX), y + initialOffsetY + r*(gapY+sizeY))


def cartCoToIsoCo(cartX, cartY):
    isoX = cartX - cartY
    isoY = (cartX + cartY)/2
    return isoX, isoY


def isoCoToCartCo(isoX, isoY):
    cartX = isoY + isoX/2
    cartY = isoY - isoX/2
    return cartX, cartY


def mouse_is_on_map(world, grid_pos, mouse_pos):
    mouse_on_panel = False
    for rect in [world.hud["up"].rect, world.hud["main"].rect, world.hud["fps"].rect, world.hud["pop"].rect]:
        if rect.collidepoint(mouse_pos):
            mouse_on_panel = True
    world_bounds = (0 <= grid_pos[0] < world.grid_lx) and (
        0 <= grid_pos[1] < world.grid_ly)
    if world_bounds and not mouse_on_panel:
        return True
    else:
        return False


def mouse_to_grid(x, y, scroll, offset):
    # remove camera scrolling & offset
    world_x = x - scroll.x - offset
    world_y = y - scroll.y
    # transform iso to cartesian
    cart_x, cart_y = isoCoToCartCo(world_x, world_y)
    # transform back to grid matrix
    grid_x = int(cart_x // TILE_SIZE)
    grid_y = int(cart_y // TILE_SIZE)
    return grid_x, grid_y


def zone_grid(drag_process, drag_start, drag_end, scroll, offset):
    if drag_process and drag_end != None and drag_start != None:
        x_start, y_start = drag_start
        x_end, y_end = drag_end
        grid_start_x, grid_start_y = mouse_to_grid(
            x_start, y_start, scroll, offset)
        grid_end_x, grid_end_y = mouse_to_grid(x_end, y_end, scroll, offset)
        # print([grid_start_x, grid_start_y], [grid_end_x, grid_end_y])
        return [grid_start_x, grid_start_y], [grid_end_x, grid_end_y]


def get_points_in_rectangle(x1, y1, x2, y2):
    if x1 == x2 and y1 == y2:
        return [(x1, y1)]
    else:
        points = []
        coef_x = 1
        coef_y = 1
        if x1 > x2:
            coef_x = -1
        if y1 > y2:
            coef_y = -1
        for x in range(x1, x2+coef_x, coef_x):
            for y in range(y1, y2+coef_y, coef_y):
                points.append((x, y))
        return points


def get_road_pathway(x1, y1, x2, y2, pathway):
    # pathway = list(dict.fromkeys(pathway))
    if x1 == x2 and y1 == y2:
        pathway.append((x1, y1))
    elif (x2, y2) not in pathway:
        pathway.append((x2, y2))

# 1 North #2 South #3 West #4 East


def get_nearby_tile(grid, direction):
    x, y = grid
    match direction:
        case "north":
            return x, y-1
        case "south":
            return x, y+1
        case "west":
            return x-1, y
        case "east":
            return x+1, y


def get_surrounding_coordinate(grid):
    grid_n = get_nearby_tile(grid, "north")
    grid_s = get_nearby_tile(grid, "south")
    grid_w = get_nearby_tile(grid, "west")
    grid_e = get_nearby_tile(grid, "east")

    return {"north": grid_n, "south": grid_s, "west": grid_w, "east": grid_e}


def set_neighborhood_likeliness(tile, world_grid):
    # print("changement being called")
    # print(f"this.grid{tile.grid}")
    nearby = get_surrounding_coordinate(tile.grid)
    # print(
    #     f"neaby :: N :{nearby['north']}, S:{nearby['south']}, W:{nearby['west']}, E:{nearby['east']}")
    cord_north = nearby["north"]
    cord_south = nearby["south"]
    cord_west = nearby["west"]
    cord_east = nearby["east"]
    # north
    # print(f"type :: N:{world_grid[cord_north[0]][cord_north[1]]}, S:{world_grid[cord_south[0]][cord_south[1]]},\
    #                 W:{world_grid[cord_west[0]][cord_west[1]]},E:{world_grid[cord_east[0]][cord_east[1]]}")
    if 0 <= cord_north[0] <= 39 and 0 <= cord_north[1] <= 39:
        if type(tile) == type(world_grid[cord_north[0]][cord_north[1]]):
            tile.north = True
        elif type(tile) != type(world_grid[cord_north[0]][cord_north[1]]):
            tile.north = False
    # elif cord_north[1] < 0:
    #     tile.north = True
        # south
    if 0 <= cord_south[0] <= 39 and 0 <= cord_south[1] <= 39:
        if type(tile) == type(world_grid[cord_south[0]][cord_south[1]]):
            tile.south = True
        elif type(tile) != type(world_grid[cord_south[0]][cord_south[1]]):
            tile.south = False
    # elif cord_south[1] > 39:
    #     tile.south = True
    # west
    if 0 <= cord_west[0] <= 39 and 0 <= cord_west[1] <= 39:
        if type(tile) == type(world_grid[cord_west[0]][cord_west[1]]):
            tile.west = True
        elif type(tile) != type(world_grid[cord_west[0]][cord_west[1]]):
            tile.west = False
    # elif cord_west[0] < 0:
    #     tile.west = True
    # east
    if 0 <= cord_east[0] <= 39 and 0 <= cord_east[1] <= 39:
        if type(tile) == type(world_grid[cord_east[0]][cord_east[1]]):
            tile.east = True
        elif type(tile) != type(world_grid[cord_east[0]][cord_east[1]]):
            tile.east = False
    # elif cord_east[0] > 39:
    #     tile.east = True

    # print(
    #     f"after change n{tile.north},s{tile.south},w{tile.west},e{tile.east}")


def road_shifting_util(road):
    n = road.north
    s = road.south
    w = road.west
    e = road.east

    # defaut

    if n and s and w and e:
        return "ALL"
    elif n and not s and not w and not e:
        return "S"
    elif not n and s and not w and not e:
        return "N"
    elif not n and not s and w and not e:
        return "E"
    elif not n and not s and not w and e:
        return "W"
    elif n and s and not w and not e:
        return "S-N"
    elif not n and not s and w and e:
        return "W-E"
    elif n and not s and not w and e:
        return "N&E"
    elif not n and s and not w and e:
        return "S&E"
    elif not n and s and w and not e:
        return "W&S"
    elif n and not s and w and not e:
        return "W&N"
    elif n and s and not w and e:
        return "N_S_E"
    elif n and s and w and not e:
        return "N_W_S"
    elif n and not s and w and e:
        return "W_N_E"
    elif not n and s and w and e:
        return "W_S_E"
    elif not n and not s and not w and not e:
        # print("S default")
        return "S"


def get_iso_polygon(iso_x, iso_y):
    return [
        (iso_x*TILE_SIZE, iso_y*TILE_SIZE),
        (iso_x*TILE_SIZE+TILE_SIZE, iso_y*TILE_SIZE),
        (iso_x*TILE_SIZE+TILE_SIZE, iso_y*TILE_SIZE+TILE_SIZE),
        (iso_x*TILE_SIZE, iso_y*TILE_SIZE+TILE_SIZE)
    ]


def get_ratio(big, small):
    return small/big

# A* pathrfinding algo
# 1er edition


def A_star(start, goal, grid=None):
    # Set of nodes already evaluated
    closed_set = set()
    # The set of currently discovered nodes that are not evaluated yet.
    open_set = {start}
    # For each node, which node it can most efficiently be reached from.
    # If a node can be reached from many nodes, came_from will eventually contain the
    # most efficient previous step.
    came_from = dict()
    # For each node, the cost of getting from the start node to that node.
    g_score = {start: 0}
    # For each node, the total cost of getting from the start node to the goal
    # by passing by that node. That value is partly known, partly heuristic.
    h_score = {start: manhattan_distance(start, goal)}
    f_score = {start: manhattan_distance(start, goal)}

    while open_set:
        current = min(open_set, key=lambda x: f_score[x])
        # current = min({k: v for k, v in f_score.items() if v <=
        #                min(f_score.values())}, key=lambda x: h_score[x])
        if current == goal:
            return reconstruct_path(came_from, current)
        open_set.remove(current)
        closed_set.add(current)

        for neighbor in neighbors(current, grid):
            # print(neighbor)
            if neighbor in closed_set:
                continue
            tentative_g_score = g_score[current] + \
                movement_cost(current, neighbor, grid)

            if neighbor not in open_set:
                open_set.add(neighbor)
            elif tentative_g_score >= g_score[neighbor]:
                continue

            came_from[neighbor] = current
            g_score[neighbor] = tentative_g_score
            h_score[neighbor] = manhattan_distance(neighbor, goal)
            f_score[neighbor] = g_score[neighbor] + h_score[neighbor]

    return None


def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    return list(reversed(total_path))
#
# 1er edition


def neighbors(current, grid):

    width, height = MAP_SIZE[0], MAP_SIZE[1]

    x, y = current
    results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]

    # results = filter(lambda x: 0 <= x[0] < width and 0 <=
    #                  x[1] < height, results)
    results = [(x, y) for (x, y) in results if 0 <=
               x < width and 0 <= y < height]
    if grid != None:
        results = [(x, y) for (x, y) in results if grid[x]
                   [y] != 'X']

    return results


def movement_cost(current, neighbor, grid):
    if grid == None:
        return 1
    else:
        cur_x, cur_y = current
        nei_x, nei_y = neighbor
        if grid[cur_x][cur_y] == True:
            if grid[nei_x][nei_y] == False:
                return 5
            elif grid[nei_x][nei_y] == True:
                return 1
        elif grid[cur_x][cur_y] == False:
            if grid[nei_x][nei_y] == False:
                return 5
            elif grid[nei_x][nei_y] == True:
                return 1
    return 1
# Test only: effacer cette manhanttan pour remplacer avec propre code distance


def manhattan_distance(current, goal):
    # Compute the Manhattan distance between two points
    return abs(current[0] - goal[0]) + abs(current[1] - goal[1])


def overlay_util(number):
    # en pourcentage
    stat = (number / FIRE_THRESHOLD)*100
    if 5 < stat < 15:
        return "15<"
    elif 15 < stat < 30:
        return "15-30"
    elif 30 < stat < 45:
        return "30-45"
    elif 45 < stat < 60:
        return "45-60"
    elif 60 < stat < 75:
        return "60-75"
    elif 75 < stat < 90:
        return "75-90"
    elif stat > 90:
        return ">90"


def polygon_center(vertices):
    x_sum = 0
    y_sum = 0
    for vertex in vertices:
        x_sum += vertex[0]
        y_sum += vertex[1]
    center_x = x_sum / len(vertices)
    center_y = y_sum / len(vertices)
    return (center_x, center_y)
