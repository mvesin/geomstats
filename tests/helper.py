"""
Helper functions for unit tests.
"""

import geomstats.backend as gs


def to_scalar(expected):
    expected = gs.to_ndarray(expected, to_ndim=1)
    expected = gs.to_ndarray(expected, to_ndim=2, axis=-1)
    return expected


def to_vector(expected):
    expected = gs.to_ndarray(expected, to_ndim=2)
    return expected


def to_matrix(expected):
    expected = gs.to_ndarray(expected, to_ndim=3)
    return expected


def left_log_then_exp_from_identity(metric, point):
    aux = metric.left_log_from_identity(point=point)
    result = metric.left_exp_from_identity(tangent_vec=aux)
    return result


def left_exp_then_log_from_identity(metric, tangent_vec):
    aux = metric.left_exp_from_identity(tangent_vec=tangent_vec)
    result = metric.left_log_from_identity(point=aux)
    return result


def log_then_exp_from_identity(metric, point):
    aux = metric.log_from_identity(point=point)
    result = metric.exp_from_identity(tangent_vec=aux)
    return result


def exp_then_log_from_identity(metric, tangent_vec):
    aux = metric.exp_from_identity(tangent_vec=tangent_vec)
    result = metric.log_from_identity(point=aux)
    return result


def log_then_exp(metric, point, base_point=None):
    aux = metric.log(point=point,
                     base_point=base_point)
    result = metric.exp(tangent_vec=aux,
                        base_point=base_point)
    return result


def exp_then_log(metric, tangent_vec, base_point=None):
    aux = metric.exp(tangent_vec=tangent_vec,
                     base_point=base_point)
    result = metric.log(point=aux,
                        base_point=base_point)
    return result


def group_log_then_exp_from_identity(group, point):
    aux = group.log_from_identity(point=point)
    result = group.exp_from_identity(tangent_vec=aux)
    return result


def group_exp_then_log_from_identity(group, tangent_vec):
    aux = group.exp_from_identity(tangent_vec=tangent_vec)
    result = group.log_from_identity(point=aux)
    return result


def group_log_then_exp(group, point, base_point):
    aux = group.log(
        point=point, base_point=base_point)
    result = group.exp(
        tangent_vec=aux, base_point=base_point)
    return result


def group_exp_then_log(group, tangent_vec, base_point):
    aux = group.exp(
        tangent_vec=tangent_vec, base_point=base_point)
    result = group.log(
        point=aux, base_point=base_point)
    return result


def test_parallel_transport(space, metric, shape):
    results = []

    def is_isometry(tan_a, trans_a, endpoint):
        is_tangent = space.is_tangent(trans_a, endpoint)
        is_equinormal = gs.isclose(
            metric.norm(trans_a), metric.norm(tan_a))
        return gs.logical_and(is_tangent, is_equinormal)

    base_point = space.random_point(shape[0])
    tan_vec_a = space.to_tangent(gs.random.rand(*shape), base_point)
    tan_vec_b = space.to_tangent(gs.random.rand(*shape), base_point)
    end_point = metric.exp(tan_vec_b, base_point)

    transported = metric.parallel_transport(
        tan_vec_a, tan_vec_b, base_point)
    result = is_isometry(tan_vec_a, transported, end_point)
    results.append(gs.all(result))

    base_point = base_point[0]
    tan_vec_a = space.to_tangent(tan_vec_a, base_point)
    tan_vec_b = space.to_tangent(tan_vec_b, base_point)
    end_point = metric.exp(tan_vec_b, base_point)
    transported = metric.parallel_transport(
        tan_vec_a, tan_vec_b, base_point)
    result = is_isometry(tan_vec_a, transported, end_point)
    results.append(gs.all(result))

    one_tan_vec_a = tan_vec_a[0]
    transported = metric.parallel_transport(
        one_tan_vec_a, tan_vec_b, base_point)
    result = is_isometry(one_tan_vec_a, transported, end_point)
    results.append(gs.all(result))

    one_tan_vec_b = tan_vec_b[0]
    end_point = end_point[0]
    transported = metric.parallel_transport(
        tan_vec_a, one_tan_vec_b, base_point)
    result = is_isometry(tan_vec_a, transported, end_point)
    results.append(gs.all(result))

    transported = metric.parallel_transport(
        one_tan_vec_a, one_tan_vec_b, base_point)
    result = is_isometry(one_tan_vec_a, transported, end_point)
    results.append(gs.all(result))

    return results
