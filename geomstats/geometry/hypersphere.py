"""The n-dimensional hypersphere.

The n-dimensional hypersphere embedded in (n+1)-dimensional
Euclidean space.
"""

import logging
from itertools import product

from scipy.stats import beta

import geomstats.algebra_utils as utils
import geomstats.backend as gs
from geomstats.geometry.embedded_manifold import EmbeddedManifold
from geomstats.geometry.euclidean import Euclidean
from geomstats.geometry.euclidean import EuclideanMetric
from geomstats.geometry.riemannian_metric import RiemannianMetric


class _Hypersphere(EmbeddedManifold):
    """Private class for the n-dimensional hypersphere.

    Class for the n-dimensional hypersphere embedded in the
    (n+1)-dimensional Euclidean space.

    By default, points are parameterized by their extrinsic
    (n+1)-coordinates.

    Parameters
    ----------
    dim : int
        Dimension of the hypersphere.
    """

    def __init__(self, dim):
        super(_Hypersphere, self).__init__(
            dim=dim,
            embedding_manifold=Euclidean(dim + 1))
        self.embedding_metric = self.embedding_manifold.metric

    def belongs(self, point, atol=gs.atol):
        """Test if a point belongs to the hypersphere.

        This tests whether the point's squared norm in Euclidean space is 1.

        Parameters
        ----------
        point : array-like, shape=[..., dim + 1]
            Point in Euclidean space.
        atol : float
            Tolerance at which to evaluate norm == 1.
            Optional, default: backend atol.

        Returns
        -------
        belongs : array-like, shape=[...,]
            Boolean evaluating if point belongs to the hypersphere.
        """
        point_dim = gs.shape(point)[-1]
        if point_dim != self.dim + 1:
            if point_dim is self.dim:
                logging.warning(
                    'Use the extrinsic coordinates to '
                    'represent points on the hypersphere.')
            belongs = False
            if gs.ndim(point) == 2:
                belongs = gs.tile([belongs], (point.shape[0],))
            return belongs
        sq_norm = gs.sum(point ** 2, axis=-1)
        diff = gs.abs(sq_norm - 1)
        return gs.less_equal(diff, atol)

    def regularize(self, point):
        """Regularize a point to the canonical representation.

        Regularize a point to the canonical representation chosen
        for the hypersphere, to avoid numerical issues.

        Parameters
        ----------
        point : array-like, shape=[..., dim + 1]
            Point on the hypersphere.

        Returns
        -------
        projected_point : array-like, shape=[..., dim + 1]
            Point in canonical representation chosen for the hypersphere.
        """
        if not gs.all(self.belongs(point)):
            raise ValueError('Points do not belong to the manifold.')

        return self.projection(point)

    def projection(self, point):
        """Project a point on the hypersphere.

        Parameters
        ----------
        point : array-like, shape=[..., dim + 1]
            Point in embedding Euclidean space.

        Returns
        -------
        projected_point : array-like, shape=[..., dim + 1]
            Point projected on the hypersphere.
        """
        norm = gs.linalg.norm(point, axis=-1)
        projected_point = gs.einsum('...,...i->...i', 1. / norm, point)

        return projected_point

    def to_tangent(self, vector, base_point):
        """Project a vector to the tangent space.

        Project a vector in Euclidean space
        on the tangent space of the hypersphere at a base point.

        Parameters
        ----------
        vector : array-like, shape=[..., dim + 1]
            Vector in Euclidean space.
        base_point : array-like, shape=[..., dim + 1]
            Point on the hypersphere defining the tangent space,
            where the vector will be projected.

        Returns
        -------
        tangent_vec : array-like, shape=[..., dim + 1]
            Tangent vector in the tangent space of the hypersphere
            at the base point.
        """
        sq_norm = gs.sum(base_point ** 2, axis=-1)
        inner_prod = self.embedding_metric.inner_product(base_point, vector)
        coef = inner_prod / sq_norm
        tangent_vec = vector - gs.einsum('...,...j->...j', coef, base_point)

        return tangent_vec

    def is_tangent(self, vector, base_point, atol=gs.atol):
        """Check whether the vector is tangent at base_point.

        Parameters
        ----------
        vector : array-like, shape=[..., dim]
            Vector.
        base_point : array-like, shape=[..., dim]
            Point on the manifold.
        atol : float
            Absolute tolerance.
            Optional, default: backend atol.

        Returns
        -------
        is_tangent : bool
            Boolean denoting if vector is a tangent vector at the base point.
        """
        inner_prod = self.embedding_metric.inner_product(base_point, vector)
        return gs.isclose(inner_prod, 0., atol=atol)

    def spherical_to_extrinsic(self, point_spherical):
        """Convert point from spherical to extrinsic coordinates.

        Convert from the spherical coordinates in the hypersphere
        to the extrinsic coordinates in Euclidean space.
        Only implemented in dimension 2.

        Parameters
        ----------
        point_spherical : array-like, shape=[..., dim]
            Point on the sphere, in spherical coordinates.

        Returns
        -------
        point_extrinsic : array_like, shape=[..., dim + 1]
            Point on the sphere, in extrinsic coordinates in Euclidean space.
        """
        if self.dim != 2:
            raise NotImplementedError(
                'The conversion from spherical coordinates'
                ' to extrinsic coordinates is implemented'
                ' only in dimension 2.')

        theta = point_spherical[..., 0]
        phi = point_spherical[..., 1]

        point_extrinsic = gs.stack(
            [gs.sin(theta) * gs.cos(phi),
             gs.sin(theta) * gs.sin(phi),
             gs.cos(theta)],
            axis=-1)

        if not gs.all(self.belongs(point_extrinsic)):
            raise ValueError('Points do not belong to the manifold.')

        return point_extrinsic

    def tangent_spherical_to_extrinsic(self, tangent_vec_spherical,
                                       base_point_spherical):
        """Convert tangent vector from spherical to extrinsic coordinates.

        Convert from the spherical coordinates in the hypersphere
        to the extrinsic coordinates in Euclidean space for a tangent
        vector. Only implemented in dimension 2.

        Parameters
        ----------
        tangent_vec_spherical : array-like, shape=[..., dim]
            Tangent vector to the sphere, in spherical coordinates.
        base_point_spherical : array-like, shape=[..., dim]
            Point on the sphere, in spherical coordinates.

        Returns
        -------
        tangent_vec_extrinsic : array-like, shape=[..., dim + 1]
            Tangent vector to the sphere, at base point,
            in extrinsic coordinates in Euclidean space.
        """
        if self.dim != 2:
            raise NotImplementedError(
                'The conversion from spherical coordinates'
                ' to extrinsic coordinates is implemented'
                ' only in dimension 2.')

        axes = (2, 0, 1) if base_point_spherical.ndim == 2 else (0, 1)
        theta = base_point_spherical[..., 0]
        phi = base_point_spherical[..., 1]

        zeros = gs.zeros_like(theta)

        jac = gs.array([
            [gs.cos(theta) * gs.cos(phi), - gs.sin(theta) * gs.sin(phi)],
            [gs.cos(theta) * gs.sin(phi), gs.sin(theta) * gs.cos(phi)],
            [- gs.sin(theta), zeros]])
        jac = gs.transpose(jac, axes)

        tangent_vec_extrinsic = gs.einsum(
            '...ij,...j->...i', jac, tangent_vec_spherical)

        return tangent_vec_extrinsic

    def intrinsic_to_extrinsic_coords(self, point_intrinsic):
        """Convert point from intrinsic to extrinsic coordinates.

        Convert from the intrinsic coordinates in the hypersphere,
        to the extrinsic coordinates in Euclidean space.

        Parameters
        ----------
        point_intrinsic : array-like, shape=[..., dim]
            Point on the hypersphere, in intrinsic coordinates.

        Returns
        -------
        point_extrinsic : array-like, shape=[..., dim + 1]
            Point on the hypersphere, in extrinsic coordinates in
            Euclidean space.
        """
        sq_coord_0 = 1. - gs.sum(point_intrinsic ** 2, axis=-1)
        if gs.any(gs.less(sq_coord_0, 0.)):
            raise ValueError('Square-root of a negative number.')
        coord_0 = gs.sqrt(sq_coord_0)

        point_extrinsic = gs.concatenate([
            coord_0[..., None], point_intrinsic], axis=-1)

        return point_extrinsic

    def extrinsic_to_intrinsic_coords(self, point_extrinsic):
        """Convert point from extrinsic to intrinsic coordinates.

        Convert from the extrinsic coordinates in Euclidean space,
        to some intrinsic coordinates in the hypersphere.

        Parameters
        ----------
        point_extrinsic : array-like, shape=[..., dim + 1]
            Point on the hypersphere, in extrinsic coordinates in
            Euclidean space.

        Returns
        -------
        point_intrinsic : array-like, shape=[..., dim]
            Point on the hypersphere, in intrinsic coordinates.
        """
        point_intrinsic = point_extrinsic[..., 1:]

        return point_intrinsic

    def _replace_values(self, samples, new_samples, indcs):
        replaced_indices = [
            i for i, is_replaced in enumerate(indcs) if is_replaced]
        value_indices = list(product(replaced_indices, range(self.dim + 1)))
        return gs.assignment(samples, gs.flatten(new_samples), value_indices)

    def random_point(self, n_samples=1, bound=1.):
        """Sample in the hypersphere from the uniform distribution.

        Parameters
        ----------
        n_samples : int
            Number of samples.
            Optional, default: 1.
        bound : unused

        Returns
        -------
        samples : array-like, shape=[..., dim + 1]
            Points sampled on the hypersphere.
        """
        return self.random_uniform(n_samples)

    def random_uniform(self, n_samples=1):
        """Sample in the hypersphere from the uniform distribution.

        Parameters
        ----------
        n_samples : int
            Number of samples.
            Optional, default: 1.

        Returns
        -------
        samples : array-like, shape=[..., dim + 1]
            Points sampled on the hypersphere.
        """
        size = (n_samples, self.dim + 1)

        samples = gs.random.normal(size=size)
        while True:
            norms = gs.linalg.norm(samples, axis=1)
            indcs = gs.isclose(norms, 0.0, atol=gs.atol)
            num_bad_samples = gs.sum(indcs)
            if num_bad_samples == 0:
                break
            new_samples = gs.random.normal(
                size=(num_bad_samples, self.dim + 1))
            samples = self._replace_values(samples, new_samples, indcs)

        samples = gs.einsum('..., ...i->...i', 1 / norms, samples)
        if n_samples == 1:
            samples = gs.squeeze(samples, axis=0)
        return samples

    def random_von_mises_fisher(
            self, mu=None, kappa=10, n_samples=1, max_iter=100):
        """Sample with the von Mises-Fisher distribution.

        This distribution corresponds to the maximum entropy distribution
        given a mean. In dimension 2, a closed form expression is available.
        In larger dimension, rejection sampling is used according to [Wood94]_

        References
        ----------
        https://en.wikipedia.org/wiki/Von_Mises-Fisher_distribution

        .. [Wood94]   Wood, Andrew T. A. “Simulation of the von Mises Fisher
                      Distribution.” Communications in Statistics - Simulation
                      and Computation, June 27, 2007.
                      https://doi.org/10.1080/03610919408813161.

        Parameters
        ----------
        mu : array-like, shape=[dim]
            Mean parameter of the distribution.
        kappa : float
            Kappa parameter of the von Mises distribution.
            Optional, default: 10.
        n_samples : int
            Number of samples.
            Optional, default: 1.
        max_iter : int
            Maximum number of trials in the rejection algorithm. In case it
            is reached, the current number of samples < n_samples is returned.
            Optional, default: 100.

        Returns
        -------
        point : array-like, shape=[n_samples, dim + 1]
            Points sampled on the sphere in extrinsic coordinates
            in Euclidean space of dimension dim + 1.
        """
        dim = self.dim

        if dim == 2:
            angle = 2. * gs.pi * gs.random.rand(n_samples)
            angle = gs.to_ndarray(angle, to_ndim=2, axis=1)
            unit_vector = gs.hstack((gs.cos(angle), gs.sin(angle)))
            scalar = gs.random.rand(n_samples)

            coord_x = 1. + 1. / kappa * gs.log(
                scalar + (1. - scalar) * gs.exp(gs.array(-2. * kappa)))
            coord_x = gs.to_ndarray(coord_x, to_ndim=2, axis=1)
            coord_yz = gs.sqrt(1. - coord_x ** 2) * unit_vector
            sample = gs.hstack((coord_x, coord_yz))

        else:
            # rejection sampling in the general case
            sqrt = gs.sqrt(4 * kappa ** 2. + dim ** 2)
            envelop_param = (-2 * kappa + sqrt) / dim
            node = (1. - envelop_param) / (1. + envelop_param)
            correction = kappa * node + dim * gs.log(1. - node ** 2)

            n_accepted, n_iter = 0, 0
            result = []
            while (n_accepted < n_samples) and (n_iter < max_iter):
                sym_beta = beta.rvs(
                    dim / 2, dim / 2, size=n_samples - n_accepted)
                sym_beta = gs.cast(sym_beta, node.dtype)
                coord_x = (1 - (1 + envelop_param) * sym_beta) / (
                    1 - (1 - envelop_param) * sym_beta)
                accept_tol = gs.random.rand(n_samples - n_accepted)
                criterion = (
                    kappa * coord_x
                    + dim * gs.log(1 - node * coord_x)
                    - correction) > gs.log(accept_tol)
                result.append(coord_x[criterion])
                n_accepted += gs.sum(criterion)
                n_iter += 1
            if n_accepted < n_samples:
                logging.warning(
                    'Maximum number of iteration reached in rejection '
                    'sampling before n_samples were accepted.')
            coord_x = gs.concatenate(result)
            coord_rest = _Hypersphere(dim - 1).random_uniform(n_accepted)
            coord_rest = gs.einsum(
                '...,...i->...i', gs.sqrt(1 - coord_x ** 2), coord_rest)
            sample = gs.concatenate([coord_x[..., None], coord_rest], axis=1)

        if mu is not None:
            sample = utils.rotate_points(sample, mu)

        return sample if (n_samples > 1) else sample[0]

    def random_riemannian_normal(
            self, mean=None, precision=None, n_samples=1, max_iter=100):
        r"""Sample from the Riemannian normal distribution.

        The Riemannian normal distribution, or spherical normal in this case,
        is defined by the probability density function (with respect to the
        Riemannian volume measure) proportional to:
        .. math::
                \exp \Big \left(- \frac{\lambda}{2} \mathtm{arccos}^2(x^T\mu)
                \Big \right)

        where :math: `\mu` is the mean and :math: `\lambda` is the isotropic
        precision. For the anisotropic case,
        :math: `\log_{\mu}(x)^T \Lambda \log_{\mu}(x)` is used instead.

        A rejection algorithm is used to sample from this distribution [Hau18]_

        Parameters
        ----------
        mean : array-like, shape=[dim]
            Mean parameter of the distribution.
            Optional, default: (0,...,0,1) (the north pole).
        precision : float or array-like, shape=[dim, dim]
            Inverse of the covariance parameter of the normal distribution.
            If a float is passed, the covariance matrix is precision times
            identity.
            Optional, default: identity.
        n_samples : int
            Number of samples.
            Optional, default: 1.
        max_iter : int
            Maximum number of trials in the rejection algorithm. In case it
            is reached, the current number of samples < n_samples is returned.
            Optional, default: 100.

        Returns
        -------
        point : array-like, shape=[n_samples, dim + 1]
            Points sampled on the sphere.

        References
        ----------
        .. [Hau18]  Hauberg, Soren. “Directional Statistics with the
                    Spherical Normal Distribution.”
                    In 2018 21st International Conference on Information
                    Fusion (FUSION), 704–11, 2018.
                    https://doi.org/10.23919/ICIF.2018.8455242.
        """
        dim = self.dim
        n_accepted, n_iter = 0, 0
        result = []
        if precision is None:
            precision_ = gs.eye(self.dim)
        elif isinstance(precision, (float, int)):
            precision_ = precision * gs.eye(self.dim)
        else:
            precision_ = precision
        precision_2 = precision_ + (dim - 1) / gs.pi * gs.eye(dim)
        tangent_cov = gs.linalg.inv(precision_2)

        def threshold(random_v):
            """Compute the acceptance threshold."""
            squared_norm = gs.sum(random_v ** 2, axis=-1)
            sinc = utils.taylor_exp_even_func(
                squared_norm, utils.sinc_close_0) ** (dim - 1)
            threshold_val = sinc * gs.exp(squared_norm * (dim - 1) / 2 / gs.pi)
            return threshold_val, squared_norm ** .5

        while (n_accepted < n_samples) and (n_iter < max_iter):
            envelope = gs.random.multivariate_normal(
                gs.zeros(dim), tangent_cov, size=(n_samples - n_accepted,))
            thresh, norm = threshold(envelope)
            proposal = gs.random.rand(n_samples - n_accepted)
            criterion = gs.logical_and(norm <= gs.pi, proposal <= thresh)
            result.append(envelope[criterion])
            n_accepted += gs.sum(criterion)
            n_iter += 1
        if n_accepted < n_samples:
            logging.warning(
                'Maximum number of iteration reached in rejection '
                'sampling before n_samples were accepted.')
        tangent_sample_intr = gs.concatenate(result)
        tangent_sample = gs.concatenate(
            [tangent_sample_intr, gs.zeros(n_accepted)[:, None]], axis=1)

        metric = HypersphereMetric(dim)
        north_pole = gs.array([0.] * dim + [1.])
        if mean is not None:
            mean_from_north = metric.log(mean, north_pole)
            tangent_sample_at_pt = metric.parallel_transport(
                tangent_sample, mean_from_north, north_pole)
        else:
            tangent_sample_at_pt = tangent_sample
            mean = north_pole
        sample = metric.exp(tangent_sample_at_pt, mean)
        return sample[0] if (n_samples == 1) else sample


class HypersphereMetric(RiemannianMetric):
    """Class for the Hypersphere Metric.

    Parameters
    ----------
    dim : int
        Dimension of the hypersphere.
    """

    def __init__(self, dim):
        super(HypersphereMetric, self).__init__(
            dim=dim,
            signature=(dim, 0))
        self.embedding_metric = EuclideanMetric(dim + 1)
        self._space = _Hypersphere(dim=dim)

    def inner_product(self, tangent_vec_a, tangent_vec_b, base_point=None):
        """Compute the inner-product of two tangent vectors at a base point.

        Parameters
        ----------
        tangent_vec_a : array-like, shape=[..., dim + 1]
            First tangent vector at base point.
        tangent_vec_b : array-like, shape=[..., dim + 1]
            Second tangent vector at base point.
        base_point : array-like, shape=[..., dim + 1], optional
            Point on the hypersphere.

        Returns
        -------
        inner_prod : array-like, shape=[...,]
            Inner-product of the two tangent vectors.
        """
        inner_prod = self.embedding_metric.inner_product(
            tangent_vec_a, tangent_vec_b, base_point)

        return inner_prod

    def squared_norm(self, vector, base_point=None):
        """Compute the squared norm of a vector.

        Squared norm of a vector associated with the inner-product
        at the tangent space at a base point.

        Parameters
        ----------
        vector : array-like, shape=[..., dim + 1]
            Vector on the tangent space of the hypersphere at base point.
        base_point : array-like, shape=[..., dim + 1], optional
            Point on the hypersphere.

        Returns
        -------
        sq_norm : array-like, shape=[..., 1]
            Squared norm of the vector.
        """
        sq_norm = self.embedding_metric.squared_norm(vector)
        return sq_norm

    def exp(self, tangent_vec, base_point):
        """Compute the Riemannian exponential of a tangent vector.

        Parameters
        ----------
        tangent_vec : array-like, shape=[..., dim + 1]
            Tangent vector at a base point.
        base_point : array-like, shape=[..., dim + 1]
            Point on the hypersphere.

        Returns
        -------
        exp : array-like, shape=[..., dim + 1]
            Point on the hypersphere equal to the Riemannian exponential
            of tangent_vec at the base point.
        """
        hypersphere = Hypersphere(dim=self.dim)
        proj_tangent_vec = hypersphere.to_tangent(tangent_vec, base_point)
        norm2 = self.embedding_metric.squared_norm(proj_tangent_vec)

        coef_1 = utils.taylor_exp_even_func(
            norm2, utils.cos_close_0, order=4)
        coef_2 = utils.taylor_exp_even_func(
            norm2, utils.sinc_close_0, order=4)
        exp = (gs.einsum('...,...j->...j', coef_1, base_point)
               + gs.einsum('...,...j->...j', coef_2, proj_tangent_vec))

        return exp

    def log(self, point, base_point, **kwargs):
        """Compute the Riemannian logarithm of a point.

        Parameters
        ----------
        point : array-like, shape=[..., dim + 1]
            Point on the hypersphere.
        base_point : array-like, shape=[..., dim + 1]
            Point on the hypersphere.

        Returns
        -------
        log : array-like, shape=[..., dim + 1]
            Tangent vector at the base point equal to the Riemannian logarithm
            of point at the base point.
        """
        inner_prod = self.embedding_metric.inner_product(base_point, point)
        cos_angle = gs.clip(inner_prod, -1., 1.)
        squared_angle = gs.arccos(cos_angle) ** 2
        coef_1_ = utils.taylor_exp_even_func(
            squared_angle, utils.inv_sinc_close_0, order=5)
        coef_2_ = utils.taylor_exp_even_func(
            squared_angle, utils.inv_tanc_close_0, order=5)
        log = (gs.einsum('...,...j->...j', coef_1_, point)
               - gs.einsum('...,...j->...j', coef_2_, base_point))

        return log

    def dist(self, point_a, point_b):
        """Compute the geodesic distance between two points.

        Parameters
        ----------
        point_a : array-like, shape=[..., dim + 1]
            First point on the hypersphere.
        point_b : array-like, shape=[..., dim + 1]
            Second point on the hypersphere.

        Returns
        -------
        dist : array-like, shape=[..., 1]
            Geodesic distance between the two points.
        """
        norm_a = self.embedding_metric.norm(point_a)
        norm_b = self.embedding_metric.norm(point_b)
        inner_prod = self.embedding_metric.inner_product(point_a, point_b)

        cos_angle = inner_prod / (norm_a * norm_b)
        cos_angle = gs.clip(cos_angle, -1, 1)

        dist = gs.arccos(cos_angle)

        return dist

    def squared_dist(self, point_a, point_b):
        """Squared geodesic distance between two points.

        Parameters
        ----------
        point_a : array-like, shape=[..., dim]
            Point on the hypersphere.
        point_b : array-like, shape=[..., dim]
            Point on the hypersphere.

        Returns
        -------
        sq_dist : array-like, shape=[...,]
        """
        return self.dist(point_a, point_b) ** 2

    @staticmethod
    def parallel_transport(tangent_vec_a, tangent_vec_b, base_point):
        r"""Compute the parallel transport of a tangent vector.

        Closed-form solution for the parallel transport of a tangent vector a
        along the geodesic defined by :math: `t \mapsto exp_(base_point)(t*
        tangent_vec_b)`.

        Parameters
        ----------
        tangent_vec_a : array-like, shape=[..., dim + 1]
            Tangent vector at base point to be transported.
        tangent_vec_b : array-like, shape=[..., dim + 1]
            Tangent vector at base point, along which the parallel transport
            is computed.
        base_point : array-like, shape=[..., dim + 1]
            Point on the hypersphere.

        Returns
        -------
        transported_tangent_vec: array-like, shape=[..., dim + 1]
            Transported tangent vector at `exp_(base_point)(tangent_vec_b)`.
        """
        theta = gs.linalg.norm(tangent_vec_b, axis=-1)
        normalized_b = gs.einsum('...,...i->...i', 1 / theta, tangent_vec_b)
        pb = gs.einsum('...i,...i->...', tangent_vec_a, normalized_b)
        p_orth = tangent_vec_a - gs.einsum('...,...i->...i', pb, normalized_b)
        transported = \
            - gs.einsum('...,...i->...i', gs.sin(theta) * pb, base_point)\
            + gs.einsum('...,...i->...i', gs.cos(theta) * pb, normalized_b)\
            + p_orth
        return transported

    def christoffels(self, point, point_type='spherical'):
        """Compute the Christoffel symbols at a point.

        Only implemented in dimension 2 and for spherical coordinates.

        Parameters
        ----------
        point : array-like, shape=[..., dim]
            Point on hypersphere where the Christoffel symbols are computed.

        point_type: str, {'spherical', 'intrinsic', 'extrinsic'}
            Coordinates in which to express the Christoffel symbols.
            Optional, default: 'spherical'.

        Returns
        -------
        christoffel : array-like, shape=[..., contravariant index, 1st
                                         covariant index, 2nd covariant index]
            Christoffel symbols at point.
        """
        if self.dim != 2 or point_type != 'spherical':
            raise NotImplementedError(
                'The Christoffel symbols are only implemented'
                ' for spherical coordinates in the 2-sphere')

        point = gs.to_ndarray(point, to_ndim=2)
        christoffel = []
        for sample in point:
            gamma_0 = gs.array(
                [[0, 0], [0, - gs.sin(sample[0]) * gs.cos(sample[0])]])
            gamma_1 = gs.array([[0, gs.cos(sample[0]) / gs.sin(sample[0])],
                                [gs.cos(sample[0]) / gs.sin(sample[0]), 0]])
            christoffel.append(gs.stack([gamma_0, gamma_1]))

        christoffel = gs.stack(christoffel)
        if gs.ndim(christoffel) == 4 and gs.shape(christoffel)[0] == 1:
            christoffel = gs.squeeze(christoffel, axis=0)
        return christoffel

    def curvature(
            self, tangent_vec_a, tangent_vec_b, tangent_vec_c,
            base_point):
        r"""Compute the curvature.

        For three tangent vectors at a base point :math: `x,y,z`,
        the curvature is defined by
        :math: `R(x, y)z = \nabla_{[x,y]}z
        - \nabla_z\nabla_y z + \nabla_y\nabla_x z`, where :math: `\nabla`
        is the Levi-Civita connection. In the case of the hypersphere,
        we have the closed formula
        :math: `R(x,y)z = \langle x, z \rangle y - \langle y,z \rangle x`.

        Parameters
        ----------
        tangent_vec_a : array-like, shape=[..., dim]
            Tangent vector at `base_point`.
        tangent_vec_b : array-like, shape=[..., dim]
            Tangent vector at `base_point`.
        tangent_vec_c : array-like, shape=[..., dim]
            Tangent vector at `base_point`.
        base_point :  array-like, shape=[..., dim]
            Point on the group. Optional, default is the identity.

        Returns
        -------
        curvature : array-like, shape=[..., dim]
            Tangent vector at `base_point`.
        """
        inner_ac = self.inner_product(tangent_vec_a, tangent_vec_c)
        inner_bc = self.inner_product(tangent_vec_b, tangent_vec_c)
        first_term = gs.einsum('...,...i->...i', inner_bc, tangent_vec_a)
        second_term = gs.einsum('...,...i->...i', inner_ac, tangent_vec_b)
        return - first_term + second_term


class Hypersphere(_Hypersphere):
    """Class for the n-dimensional hypersphere.

    Class for the n-dimensional hypersphere embedded in the
    (n+1)-dimensional Euclidean space.

    By default, points are parameterized by their extrinsic
    (n+1)-coordinates.

    Parameters
    ----------
    dim : int
        Dimension of the hypersphere.
    """

    def __init__(self, dim):
        super(Hypersphere, self).__init__(dim)
        self.metric = HypersphereMetric(dim)
