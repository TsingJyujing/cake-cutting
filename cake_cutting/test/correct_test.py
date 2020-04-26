import logging
import random
import unittest

import numpy

from cake_cutting import MatrixShape, arrangement_algorithm

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__file__)


class CorrectionTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.data = {
            f"im-{i}": MatrixShape(random.randint(200, 300), random.randint(200, 300))
            for i in range(random.randint(3, 10))
        }
        cls.padding_size = MatrixShape(10, 10)
        cls.container_size = MatrixShape(120, 120)
        cls.cake_containers = arrangement_algorithm(
            matrixes=cls.data,
            container_size=cls.container_size,
            padding_size=cls.padding_size
        )

    def test_all_container_size_correct(self):
        for container_id, cake_container in enumerate(self.cake_containers):
            if cake_container.container_size != self.container_size:
                raise Exception("Container #{} size not correct.".format(container_id))

    def test_containers_overlapping(self):
        all_sum_piece_area = 0
        all_container_area = 0
        for container_id, cake_container in enumerate(self.cake_containers):
            sum_piece_area = sum(piece.area for piece in cake_container.pieces)
            container_area = cake_container.container_size.area
            overlapping_detection = numpy.zeros(cake_container.container_size.tuple)
            for piece in cake_container.pieces:
                container_location = piece.container_loc
                overlapping_detection[
                container_location.left:container_location.left + container_location.width,
                container_location.top:container_location.top + container_location.height
                ] += 1
            if numpy.any(overlapping_detection > 1):
                raise Exception()
            else:
                all_sum_piece_area += sum_piece_area
                all_container_area += container_area
                log.info("No overlapping in container {} utilize rate={}/{}={}%".format(
                    container_id, sum_piece_area, container_area, sum_piece_area * 100.0 / container_area
                ))
        log.info("No overlapping in all container, utilize rate={}/{}={}%".format(
            all_sum_piece_area, all_container_area, all_sum_piece_area * 100.0 / all_container_area
        ))

    def test_no_missing(self):
        images = {
            k: numpy.zeros(s.tuple)
            for k, s in self.data.items()
        }
        for cake_container in self.cake_containers:
            for piece_mapping in cake_container.pieces:
                mat_id = piece_mapping.original_id
                original_location = piece_mapping.original_loc
                images[mat_id][
                original_location.left:original_location.left + original_location.width,
                original_location.top:original_location.top + original_location.height
                ] += 1
        for mat_id, image in images.items():
            if numpy.any(image <= 0):
                raise Exception("Some pixel uncovered in mat: {}".format(mat_id))
            else:
                log.info("All pixel covered in image {}".format(mat_id))

    def test_no_missing_with_padding(self):
        images = {
            k: numpy.zeros(s.tuple)
            for k, s in self.data.items()
        }
        for cake_container in self.cake_containers:
            for piece_mapping in cake_container.pieces:
                mat_id = piece_mapping.original_id
                original_location = piece_mapping.original_loc
                x_start = original_location.left + self.padding_size.width
                x_end = original_location.left + original_location.width - self.padding_size.width
                y_start = original_location.top + self.padding_size.height
                y_end = original_location.top + original_location.height - self.padding_size.height
                images[mat_id][x_start:x_end, y_start:y_end] += 1
        for mat_id, image in images.items():
            im_clip = image[
                      self.padding_size.width:-self.padding_size.width,
                      self.padding_size.height:-self.padding_size.height
                      ]
            if numpy.any(im_clip <= 0):
                raise Exception("Some pixel uncovered in mat: {}".format(mat_id))
            else:
                log.info("All pixel without padding covered in image {}".format(mat_id))
