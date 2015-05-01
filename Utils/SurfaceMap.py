__author__ = 'beniamin'

from random import choice, randint
from Utils.Exceptions import NoEmptyXYFound


class SurfaceMap():

    def __init__(self, width, height):
        self.map = []
        self.width = width
        self.height = height
        self.regions = []
        for x in xrange(width):
            tmp = []
            for y in xrange(height):
                tmp.append(False)
            self.map.append(tmp)
        for x in xrange(width / 25):
            tmp = []
            for y in xrange(height / 25):
                tmp.append([])
            self.regions.append(tmp)

    def xy_is_in_map(self, x, y):
        return not (x >= self.width or y >= self.height or x < 0 or y < 0)

    def rect_is_in_map(self, rect):
        return not (rect.x + rect.width > self.width or rect.y + rect.height > self.height or rect.x < 0 or rect.y < 0)

    def get(self, x, y):
        """Return single point from map"""
        return self.map[x][y]

    def get_corners_rect(self, rect, x=0, y=0):
        """Return tuple of 4 corners of given rect moved by x, y"""
        try:
            return (self.map[rect.x + x][rect.y + y],
                    self.map[rect.x + rect.width - 1 + x][rect.y + y],
                    self.map[rect.x + x][rect.y + rect.height - 1 + y],
                    self.map[rect.x + rect.width - 1 + x][rect.y + rect.height - 1 + y])
        except IndexError as e:
            print rect.x, rect.width, rect.y, rect.height, x, y
            raise e

    def is_empty_rect_border(self, rect, x=0, y=0):
        """Return true if all points on rect border moved by x, y are empty"""
        # Horizontal borders
        for _x in xrange(rect.width):
            if self.map[rect.x + x + _x][rect.y + y] or self.map[rect.x + x + _x][rect.y + y + rect.height - 1]:
                return False
            # Vertical borders
        for _y in xrange(rect.height - 2):
            if self.map[rect.x + x][rect.y + y + _y + 1] or self.map[rect.x + x + rect.width - 1][rect.y + y + _y + 1]:
                return False
        return True

    def is_empty_or_obj_rect_border(self, rect, obj, x=0, y=0):
        """Return true if all points on rect border moved by x, y are empty or point obj"""
        # Horizontal borders
        for _x in xrange(rect.width):
            border_top = self.map[rect.x + x + _x][rect.y + y]
            border_bottom = self.map[rect.x + x + _x][rect.y + y + rect.height - 1]
            if border_top and border_top != obj or border_bottom and border_bottom != obj:
                return False
            # Vertical borders
        for _y in xrange(rect.height - 2):
            border_left = self.map[rect.x + x][rect.y + y + _y + 1]
            border_right = self.map[rect.x + x + rect.width - 1][rect.y + y + _y + 1]
            if border_left and border_left != obj or border_right and border_right != obj:
                return False
        return True

    def get_corners_xy(self, x, y, width, height):
        """Return tuple of 4 corners of given x, y and x+width, y+height"""
        try:
            return (self.map[x][y],
                    self.map[x + width - 1][y],
                    self.map[x][y + height - 1],
                    self.map[x + width - 1][y + height - 1])
        except IndexError as e:
            print x, y, width, height
            raise e

    def is_empty_rect(self, rect):
        """Return true if all points inside rect are empty"""
        for _x in xrange(rect.width):
            for _y in xrange(rect.height):
                try:
                    if self.map[rect.x + _x][rect.y + _y]:
                        return False
                except IndexError:
                    pass
        return True

    def is_empty_xy_rect(self, x, y, size):
        """Return true if all points inside rect are empty"""
        for _x in xrange(size):
            for _y in xrange(size):
                try:
                    if self.map[x + _x][y + _y]:
                        return False
                except IndexError:
                    pass
        return True

    def set_rect(self, rect, obj):
        """Set all points inside rect to point to obj, add obj to region and return this region"""
        for _x in xrange(rect.width):
            for _y in xrange(rect.height):
                self.map[rect.x + _x][rect.y + _y] = obj
        x = rect.centerx / 25
        y = rect.centery / 25
        self.regions[x][y].append(obj)
        return self.    regions[x][y]

    def unset_rect(self, rect, obj):
        """Clear all points inside rect (set False) and remove obj from region"""
        for _x in xrange(rect.width):
            for _y in xrange(rect.height):
                self.map[rect.x + _x][rect.y + _y] = False
        x = rect.centerx / 25
        y = rect.centery / 25
        self.regions[x][y].remove(obj)

    def update_region(self, rect, obj):
        """Set all points inside rect to point to obj, add obj to region and return this region"""
        x = rect.centerx / 25
        y = rect.centery / 25
        #FIXME: list index out of range
        try:
            self.regions[x][y]
        except IndexError as e:
            print e, x, y, rect
            import pdb; pdb.set_trace()
        if obj.map_region != self.regions[x][y]:
            obj.map_region.remove(obj)
            self.regions[x][y].append(obj)
            obj.map_region = self.regions[x][y]
        return self.regions[x][y]

    def set_col(self, x, y, height, obj):
        for _y in xrange(height):
            self.map[x][y + _y] = obj

    def unset_col(self, x, y, height):
        for _y in xrange(height):
            self.map[x][y + _y] = None

    def set_row(self, x, y, width, obj):
        for _x in xrange(width):
            self.map[x + _x][y] = obj

    def unset_row(self, x, y, width):
        for _x in xrange(width):
            self.map[x + _x][y] = None

    def get_all_elements_in_region(self, pt_x, pt_y):
        """Return list of objects in region contains point(pt_x, pt_y)"""
        region_x = pt_x / 25
        region_y = pt_y / 25
        return self.regions[region_x][region_y]

    def get_empty_sibling(self, rect, empty_size=None):
        """Return one random empty sibling x, y"""
        if empty_size is None:
            empty_size = rect.width
        siblings = ((rect.x, rect.y - empty_size),
                               (rect.x + rect.width, rect.y),
                               (rect.x, rect.y + rect.height),
                               (rect.x - empty_size, rect.y))
        empty_siblings = []
        for sibling in siblings:
            if sibling[0] >= 0 and sibling[1] >= 0 and \
                    sibling[0] + empty_size + 1 < self.width and sibling[1] + empty_size + 1 < self.height and \
                    not any(self.get_corners_xy(sibling[0], sibling[1], empty_size, empty_size)) and \
                    self.is_empty_xy_rect(sibling[0], sibling[1], empty_size):
                empty_siblings.append(sibling)
        siblings_len = len(empty_siblings)
        if siblings_len > 1:
            return choice(empty_siblings)
        elif siblings_len == 1:
            return empty_siblings[0]
        else:
            return None

    def find_empty_xy_randomly(self, min_x, max_x, min_y, max_y, size):
        x = randint(min_x, max_x)
        y = randint(min_y, max_y)
        counter = 0
        while any(self.get_corners_xy(x, y, size, size)) or not self.is_empty_xy_rect(x, y, size):
            x = randint(min_x, max_x)
            y = randint(min_y, max_y)
            if counter > 100:
                raise NoEmptyXYFound()
            counter += 1
        return x, y



