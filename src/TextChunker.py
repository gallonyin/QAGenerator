"""
    TextChunker
    目标：按照句号分割，可以保证分割两侧句子的完整性，同时让两段内容之间有一定的重叠。
"""
import re


class TextChunker:
    class ChunkInfo:
        def __init__(self, chunks, tokens):
            self.chunks = chunks
            self.tokens = tokens

    @staticmethod
    def split_text_into_chunks(text, max_len):
        overlap_len = int(max_len * 0.25)  # 重叠长度

        try:
            split_texts = re.split(r'(?<=[。！？；.!?;])', text)  # 使用正则表达式分割文本成句子
            chunks = []
            pre_chunk = ""
            chunk = ""
            tokens = 0

            for sentence in split_texts:
                chunk += sentence

                if len(chunk) > max_len - overlap_len:
                    pre_chunk += sentence

                if len(chunk) >= max_len:
                    chunks.append(chunk)
                    tokens += TextChunker.count_prompt_tokens(chunk, "system")  # 计算令牌数量
                    chunk = pre_chunk
                    pre_chunk = ""

            if chunk:
                chunks.append(chunk)
                tokens += TextChunker.count_prompt_tokens(chunk, "system")  # 计算令牌数量

            return TextChunker.ChunkInfo(chunks, tokens)
        except Exception as e:
            raise RuntimeError(e)

    @staticmethod
    def count_prompt_tokens(text, _type):
        # 在这里实现你的令牌计数逻辑
        # 此函数根据指定的类型计算块中的令牌数量
        # 你应该替换此部分以实现实际的令牌计数逻辑
        return 0


if __name__ == "__main__":
    input_text = "这是一个示例文本。它包含多个句子。每个句子都不应被拆分。块的最大长度为30个字符或更少。运行应输出测试结果。"
    max_chunk_length = 30  # 该值为每个分块的最大长度 应使用模型最大token长度*0.4 （fastGPT为0.45，并且单次生成25个问答对，但如果希望生成尽可能多的问答对，则可以保留更多的token给输出内容）

    chunk_info = TextChunker.split_text_into_chunks(input_text, max_chunk_length)
    chunks = chunk_info.chunks
    tokens = chunk_info.tokens

    print("总令牌数：", tokens)
    for i, chunk in enumerate(chunks):
        print(f"块 {i + 1}：")
        print(chunk)
        print()