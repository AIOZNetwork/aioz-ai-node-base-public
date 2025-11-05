import my_ai_lib
from aioz_ainode_adapter.schemas import InputObject


def main():
    input_obj = InputObject(input_image="wiki/aioz.png", example_param="example")
    output_obj = my_ai_lib.run(input_obj)
    print(f"Output: {output_obj}")


if __name__ == '__main__':
    main()
