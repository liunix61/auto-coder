import byzerllm
from typing import List,Dict,Any,Optional
import argparse 
from autocoder.common import AutoCoderArgs
from autocoder.dispacher import Dispacher 
import yaml   

def parse_args() -> AutoCoderArgs:
    parser = argparse.ArgumentParser(description="Auto-implement missing methods in a Python script.")
    parser.add_argument("--source_dir", required=False, help="Path to the project")
    parser.add_argument("--git_url", help="URL of the git repository") 
    parser.add_argument("--target_file", required=False, help="the file to write the source code to")
    parser.add_argument("--query", help="the instruction to handle the source code")
    parser.add_argument("--template", default="common", help="the instruction to handle the source code")
    parser.add_argument("--project_type", default="py", help="the type of the project. py, ts, py-script, translate, or file suffix. default is py")
    parser.add_argument("--execute", action='store_true', help="Execute command line or not")
    parser.add_argument("--package_name", default="", help="only works for py-script project type. The package name of the script. default is empty.")
    parser.add_argument("--script_path", default="", help="only works for py-script project type. The path to the Python script. default is empty.")  
    parser.add_argument("--model", default="", help="the model name to use")
    parser.add_argument("--model_max_length", type=int, default=1024, help="the maximum length generated by the model. default is 1024 this only works when model is specified.")
    parser.add_argument("--file", help="Path to the YAML configuration file")
    parser.add_argument("--anti_quota_limit",type=int, default=1, help="After how much time to wait for the next request. default is 1s")
    
    args = parser.parse_args()
    return AutoCoderArgs(**vars(args))


def main():
    args = parse_args()
    if args.file:
        with open(args.file, "r") as f:
            config = yaml.safe_load(f)
            for key, value in config.items():
                if key != "file":  # 排除 --file 参数本身
                    setattr(args, key, value)
    
    if args.model:
        byzerllm.connect_cluster()
        llm = byzerllm.ByzerLLM()
        llm.setup_template(model=args.model,template="auto")
        llm.setup_default_model_name(args.model)
        llm.setup_max_output_length(args.model,args.model_max_length)
        llm.setup_extra_generation_params(args.model, {"max_length": args.model_max_length})
    else:
        llm = None

    dispacher = Dispacher(args, llm)
    dispacher.dispach()

if __name__ == "__main__":
    main()
