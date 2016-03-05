import draw
import save_as_image

a_maze = draw.Maze(40)
a_maze.draw_maze()

a_maze_map = a_maze.get_maze_map()
a_goal = a_maze.get_goal()

save_as_image.init(a_maze_map,a_goal)