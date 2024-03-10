import math

class Tracker:
    def __init__(self):
        # Stores the central positions of the objects
        self.center_points = {}
        # Keeps track of the IDs
        # each time a new object is detected, the count will increase by one
        self.id_count = 0

    def update(self, objects_rect):
        # Boxes and IDs of the objects
        objects_bbs_ids = []

        # Get the central point of the new object
        for rect in objects_rect:
            x, y, w, h = rect
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2

            # Check if that object has already been detected
            same_object_detected = False
            for obj_id, pt in self.center_points.items():
                dist = math.hypot(cx - pt[0], cy - pt[1])

                if dist < 5:
                    self.center_points[obj_id] = (cx, cy)
                    # print(self.center_points)
                    objects_bbs_ids.append([x, y, w, h, obj_id])
                    same_object_detected = True
                    break

            # A new object is detected, assign the ID to that object
            if not same_object_detected:
                self.center_points[self.id_count] = (cx, cy)
                objects_bbs_ids.append([x, y, w, h, self.id_count])
                self.id_count += 1

        # Clean the dictionary of central points to remove unused IDs
        new_centers = {}
        for obj_bb_id in objects_bbs_ids:
            _, _, _, _, object_id = obj_bb_id
            center = self.center_points[object_id]
            new_centers[object_id] = center

        # Update the dictionary with unused IDs removed
        self.center_points = new_centers.copy()
        return objects_bbs_ids
