import pytest

from jina import Executor, requests, __default_executor__
from jina import Flow
from tests import random_docs


@pytest.mark.parametrize('protocol', ['websocket', 'grpc', 'http'])
def test_flow(protocol):
    docs = random_docs(10)
    f = Flow(protocol=protocol).add(name='p1')

    with f:
        f.index(docs)
        assert f.num_deployments == 2
        assert f._deployment_nodes['p1'].num_pods == 2
        assert f.num_pods == 3


class MyExec(Executor):
    @requests
    def foo(self, **kwargs):
        pass


@pytest.mark.slow
@pytest.mark.parametrize('protocol', ['websocket', 'grpc', 'http'])
def test_flow_before(protocol):
    docs = random_docs(10)
    f = Flow(protocol=protocol).add(uses_before=MyExec, name='p1')

    with f:
        f.index(docs)
        assert f.num_deployments == 2
        assert f._deployment_nodes['p1'].num_pods == 3
        assert f.num_pods == 4


@pytest.mark.slow
@pytest.mark.parametrize('protocol', ['websocket', 'grpc', 'http'])
def test_flow_after(protocol):
    docs = random_docs(10)
    f = Flow(protocol=protocol).add(uses_after=MyExec, name='p1')

    with f:
        f.index(docs)
        assert f.num_deployments == 2
        assert f._deployment_nodes['p1'].num_pods == 3
        assert f.num_pods == 4


@pytest.mark.slow
@pytest.mark.parametrize('protocol', ['websocket', 'grpc', 'http'])
def test_flow_default_before_after_is_ignored(protocol):
    docs = random_docs(10)
    f = Flow(protocol=protocol).add(
        uses_after=__default_executor__, uses_before=__default_executor__, name='p1'
    )

    with f:
        f.index(docs)
        assert f.num_deployments == 2
        assert f._deployment_nodes['p1'].num_pods == 2
        assert f.num_pods == 3


@pytest.mark.slow
@pytest.mark.parametrize('protocol', ['websocket', 'grpc', 'http'])
def test_flow_before_after(protocol):
    docs = random_docs(10)
    f = Flow(protocol=protocol).add(uses_before=MyExec, uses_after=MyExec, name='p1')

    with f:
        f.index(docs)
        assert f.num_deployments == 2
        assert f._deployment_nodes['p1'].num_pods == 4
        assert f.num_pods == 5
