import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
import utils3d
import numpy as np
import torch

def run():
    for i in range(100):
        if i == 0:
            spatial = []
        else:
            dim = np.random.randint(4)
            spatial = [np.random.randint(1, 10) for _ in range(dim)]
        focal_x = np.random.uniform(0, 10, spatial)
        focal_y = np.random.uniform(0, 10, spatial)
        center_x = np.random.uniform(0, 1, spatial)
        center_y = np.random.uniform(0, 1, spatial)
        eye = np.random.uniform(-10, 10, [*spatial, 3])
        lookat = np.random.uniform(-10, 10, [*spatial, 3])
        up = np.random.uniform(-10, 10, [*spatial, 3])
        points = np.random.uniform(-10, 10, [*spatial, 3])
        
        expected, _ = utils3d.numpy.project_cv(points,
                                            utils3d.numpy.extrinsic_look_at(eye, lookat, up),
                                            utils3d.numpy.intrinsic(focal_x, focal_y, center_x, center_y))

        device = [torch.device('cpu'), torch.device('cuda')][np.random.randint(2)]
        focal_x = torch.tensor(focal_x, device=device)
        focal_y = torch.tensor(focal_y, device=device)
        center_x = torch.tensor(center_x, device=device)
        center_y = torch.tensor(center_y, device=device)
        eye = torch.tensor(eye, device=device)
        lookat = torch.tensor(lookat, device=device)
        up = torch.tensor(up, device=device)
        points = torch.tensor(points, device=device)

        actual, _ = utils3d.torch.project_cv(points,
                                            utils3d.torch.extrinsic_look_at(eye, lookat, up),
                                            utils3d.torch.intrinsic(focal_x, focal_y, center_x, center_y)
        )
        actual = actual.cpu().numpy()
        
        assert np.allclose(expected, actual), '\n' + \
            'Input:\n' + \
            f'\tfocal_x: {focal_x}\n' + \
            f'\tfocal_y: {focal_y}\n' + \
            f'\tcenter_x: {center_x}\n' + \
            f'\tcenter_y: {center_y}\n' + \
            f'\teye: {eye}\n' + \
            f'\tlookat: {lookat}\n' + \
            f'\tup: {up}\n' + \
            f'\tpoints: {points}\n' + \
            'Actual:\n' + \
            f'{actual}\n' + \
            'Expected:\n' + \
            f'{expected}'