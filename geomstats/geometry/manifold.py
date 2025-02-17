"""Manifold module.

In other words, a topological space that locally resembles
Euclidean space near each point.
"""

import geomstats.backend as gs
import geomstats.errors


class Manifold:
    r"""Class for manifolds.

    Parameters
    ----------
    dim : int
        Dimension of the manifold.
    default_point_type : str, {\'vector\', \'matrix\'}
        Point type.
        Optional, default: 'vector'.
    default_coords_type : str, {\'intrinsic\', \'extrinsic\', etc}
        Coordinate type.
        Optional, default: 'intrinsic'.
    """

    def __init__(
            self, dim, default_point_type='vector',
            default_coords_type='intrinsic', **kwargs):
        super(Manifold, self).__init__(**kwargs)
        geomstats.errors.check_integer(dim, 'dim')
        geomstats.errors.check_parameter_accepted_values(
            default_point_type, 'default_point_type', ['vector', 'matrix'])

        self.dim = dim
        self.default_point_type = default_point_type
        self.default_coords_type = default_coords_type

    def belongs(self, point, atol=gs.atol):
        """Evaluate if a point belongs to the manifold.

        Parameters
        ----------
        point : array-like, shape=[..., dim]
            Point to evaluate.
        atol : float
            Absolute tolerance.
            Optional, default: backend atol.

        Returns
        -------
        belongs : array-like, shape=[...,]
            Boolean evaluating if point belongs to the manifold.
        """
        raise NotImplementedError('belongs is not implemented.')

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
        raise NotImplementedError(
            'is_tangent is not implemented.')

    def to_tangent(self, vector, base_point):
        """Project a vector to a tangent space of the manifold.

        Parameters
        ----------
        vector : array-like, shape=[..., dim]
            Vector.
        base_point : array-like, shape=[..., dim]
            Point on the manifold.

        Returns
        -------
        tangent_vec : array-like, shape=[..., dim]
            Tangent vector at base point.
        """
        raise NotImplementedError(
            'to_tangent is not implemented.')

    def random_point(self, n_samples=1, bound=1.):
        """Sample random points on the manifold.

        If the manifold is compact, a uniform distribution is used.

        Parameters
        ----------
        n_samples : int
            Number of samples.
            Optional, default: 1.
        bound : float
            Bound of the interval in which to sample for non compact manifolds.
            Optional, default: 1.

        Returns
        -------
        samples : array-like, shape=[..., {dim, [n, n]}]
            Points sampled on the hypersphere.
        """
        raise NotImplementedError('random_point is not implemented')

    def regularize(self, point):
        """Regularize a point to the canonical representation for the manifold.

        Parameters
        ----------
        point : array-like, shape=[..., dim]
            Point.

        Returns
        -------
        regularized_point : array-like, shape=[..., dim]
            Regularized point.
        """
        regularized_point = point
        return regularized_point
