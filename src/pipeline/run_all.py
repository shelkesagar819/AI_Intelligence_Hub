
from src.pipeline.pipeline_controller import PipelineController


def run_all():

    controller = PipelineController()

    return controller.execute_all()


if __name__ == "__main__":

    run_all()
