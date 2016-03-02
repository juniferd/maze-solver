import draw
import save_as_image

a_maze = draw.Maze(50)
a_maze.draw_maze()

a_maze_map = a_maze.get_maze_map()

save_as_image.init(a_maze_map)