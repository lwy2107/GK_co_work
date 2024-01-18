from tkintermapview.canvas_path import CanvasPath
from tkintermapview.canvas_position_marker import CanvasPositionMarker
import tkinter

class CanvasPath(CanvasPath):

    def draw(self, move=False):
            new_line_length = self.last_position_list_length != len(self.position_list)
            self.last_position_list_length = len(self.position_list)

            widget_tile_width = self.map_widget.lower_right_tile_pos[0] - self.map_widget.upper_left_tile_pos[0]
            widget_tile_height = self.map_widget.lower_right_tile_pos[1] - self.map_widget.upper_left_tile_pos[1]

            if move is True and self.last_upper_left_tile_pos is not None and new_line_length is False:
                x_move = ((self.last_upper_left_tile_pos[0] - self.map_widget.upper_left_tile_pos[0]) / widget_tile_width) * self.map_widget.width
                y_move = ((self.last_upper_left_tile_pos[1] - self.map_widget.upper_left_tile_pos[1]) / widget_tile_height) * self.map_widget.height

                for i in range(0, len(self.position_list)* 2, 2):
                    self.canvas_line_positions[i] += x_move
                    self.canvas_line_positions[i + 1] += y_move
            else:
                self.canvas_line_positions = []
                for position in self.position_list:
                    canvas_position = self.get_canvas_pos(position, widget_tile_width, widget_tile_height)
                    self.canvas_line_positions.append(canvas_position[0])
                    self.canvas_line_positions.append(canvas_position[1])

            if not self.deleted:
                if self.canvas_line is None:
                    self.map_widget.canvas.delete(self.canvas_line)
                    self.canvas_line = self.map_widget.canvas.create_line(self.canvas_line_positions,
                                                                        width=3, fill='gray',
                                                                        dash=(5,1), joinstyle=tkinter.ROUND,
                                                                        arrow=tkinter.LAST, arrowshape=(13,15,7),
                                                                        tag="path")

                    if self.command is not None:
                        self.map_widget.canvas.tag_bind(self.canvas_line, "<Enter>", self.mouse_enter)
                        self.map_widget.canvas.tag_bind(self.canvas_line, "<Leave>", self.mouse_leave)
                        self.map_widget.canvas.tag_bind(self.canvas_line, "<Button-1>", self.click)
                else:
                    try:
                        self.map_widget.canvas.coords(self.canvas_line, self.canvas_line_positions)
                    except Exception:
                        pass
            else:
                self.map_widget.canvas.delete(self.canvas_line)
                self.canvas_line = None

            self.map_widget.manage_z_order()
            self.last_upper_left_tile_pos = self.map_widget.upper_left_tile_pos


class CanvasPositionMarker(CanvasPositionMarker):
    def draw(self, event=None):
            canvas_pos_x, canvas_pos_y = self.get_canvas_pos(self.position)
            canvas_pos_y = canvas_pos_y -11
            #canvas_pos_x = canvas_pos_x - 0.000095

            if not self.deleted:
                if 0 - 50 < canvas_pos_x < self.map_widget.width + 50 and 0 < canvas_pos_y < self.map_widget.height + 70:

                    # draw icon image for marker
                    if self.icon is not None:
                        if self.canvas_icon is None:
                            self.canvas_icon = self.map_widget.canvas.create_image(canvas_pos_x, canvas_pos_y,
                                                                                anchor=self.icon_anchor,
                                                                                image=self.icon,
                                                                                tag="marker")
                            if self.command is not None:
                                self.map_widget.canvas.tag_bind(self.canvas_icon, "<Enter>", self.mouse_enter)
                                self.map_widget.canvas.tag_bind(self.canvas_icon, "<Leave>", self.mouse_leave)
                                self.map_widget.canvas.tag_bind(self.canvas_icon, "<Button-1>", self.click)
                        else:
                            self.map_widget.canvas.coords(self.canvas_icon, canvas_pos_x, canvas_pos_y)

                    # draw standard icon shape
                    else:
                        if self.polygon is None:
                            self.polygon = self.map_widget.canvas.create_polygon(canvas_pos_x - 14, canvas_pos_y - 23,
                                                                                canvas_pos_x, canvas_pos_y,
                                                                                canvas_pos_x + 14, canvas_pos_y - 23,
                                                                                fill=self.marker_color_outside, width=2,
                                                                                outline=self.marker_color_outside, tag="marker")
                            if self.command is not None:
                                self.map_widget.canvas.tag_bind(self.polygon, "<Enter>", self.mouse_enter)
                                self.map_widget.canvas.tag_bind(self.polygon, "<Leave>", self.mouse_leave)
                                self.map_widget.canvas.tag_bind(self.polygon, "<Button-1>", self.click)
                        else:
                            self.map_widget.canvas.coords(self.polygon,
                                                        canvas_pos_x - 14, canvas_pos_y - 23,
                                                        canvas_pos_x, canvas_pos_y,
                                                        canvas_pos_x + 14, canvas_pos_y - 23)
                        if self.big_circle is None:
                            self.big_circle = self.map_widget.canvas.create_oval(canvas_pos_x - 14, canvas_pos_y - 45,
                                                                                canvas_pos_x + 14, canvas_pos_y - 17,
                                                                                fill=self.marker_color_circle, width=6,
                                                                                outline=self.marker_color_outside, tag="marker")
                            if self.command is not None:
                                self.map_widget.canvas.tag_bind(self.big_circle, "<Enter>", self.mouse_enter)
                                self.map_widget.canvas.tag_bind(self.big_circle, "<Leave>", self.mouse_leave)
                                self.map_widget.canvas.tag_bind(self.big_circle, "<Button-1>", self.click)
                        else:
                            self.map_widget.canvas.coords(self.big_circle,
                                                        canvas_pos_x - 14, canvas_pos_y - 45,
                                                        canvas_pos_x + 14, canvas_pos_y - 17)

                    if self.text is not None:
                        if self.canvas_text is None:
                            self.canvas_text = self.map_widget.canvas.create_text(canvas_pos_x, canvas_pos_y + self.text_y_offset,
                                                                                anchor=tkinter.S,
                                                                                text=self.text,
                                                                                fill=self.text_color,
                                                                                font=self.font,
                                                                                tag=("marker", "marker_text"))
                            if self.command is not None:
                                self.map_widget.canvas.tag_bind(self.canvas_text, "<Enter>", self.mouse_enter)
                                self.map_widget.canvas.tag_bind(self.canvas_text, "<Leave>", self.mouse_leave)
                                self.map_widget.canvas.tag_bind(self.canvas_text, "<Button-1>", self.click)
                        else:
                            self.map_widget.canvas.coords(self.canvas_text, canvas_pos_x, canvas_pos_y + self.text_y_offset)
                            self.map_widget.canvas.itemconfig(self.canvas_text, text=self.text)
                    else:
                        if self.canvas_text is not None:
                            self.map_widget.canvas.delete(self.canvas_text)

                    if self.image is not None and self.image_zoom_visibility[0] <= self.map_widget.zoom <= self.image_zoom_visibility[1]\
                            and not self.image_hidden:

                        if self.canvas_image is None:
                            self.canvas_image = self.map_widget.canvas.create_image(canvas_pos_x, canvas_pos_y + (self.text_y_offset - 30),
                                                                                    anchor=tkinter.S,
                                                                                    image=self.image,
                                                                                    tag=("marker", "marker_image"))
                        else:
                            self.map_widget.canvas.coords(self.canvas_image, canvas_pos_x, canvas_pos_y + (self.text_y_offset - 30))
                    else:
                        if self.canvas_image is not None:
                            self.map_widget.canvas.delete(self.canvas_image)
                            self.canvas_image = None
                else:
                    self.map_widget.canvas.delete(self.canvas_icon)
                    self.map_widget.canvas.delete(self.canvas_text)
                    self.map_widget.canvas.delete(self.polygon)
                    self.map_widget.canvas.delete(self.big_circle)
                    self.map_widget.canvas.delete(self.canvas_image)
                    self.canvas_text, self.polygon, self.big_circle, self.canvas_image, self.canvas_icon = None, None, None, None, None

                self.map_widget.manage_z_order()