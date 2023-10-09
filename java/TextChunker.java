import java.util.ArrayList;
import java.util.List;

/**
 * TextChunker
 * 按照句号分割，可以保证分割两侧句子的完整性，同时让两段内容之间有一定的重叠。
 */
public class TextChunker {
    public static class ChunkInfo {
        private final List<String> chunks;
        private final int tokens;

        public ChunkInfo(List<String> chunks, int tokens) {
            this.chunks = chunks;
            this.tokens = tokens;
        }

        public List<String> getChunks() {
            return chunks;
        }

        public int getTokens() {
            return tokens;
        }
    }

    public static ChunkInfo splitTextIntoChunks(String text, int maxLen) {
        int overlapLen = (int) (maxLen * 0.25); // 重叠长度

        try {
            String[] splitTexts = text.split("(?<=[。！？；.!?;])"); // 使用正则表达式分割文本成句子
            List<String> chunks = new ArrayList<>();

            String preChunk = "";
            String chunk = "";
            int tokens = 0;

            for (String sentence : splitTexts) {
                chunk += sentence;

                if (chunk.length() > maxLen - overlapLen) {
                    preChunk += sentence;
                }

                if (chunk.length() >= maxLen) {
                    chunks.add(chunk);
                    tokens += countPromptTokens(chunk, "system"); // 计算令牌数量
                    chunk = preChunk;
                    preChunk = "";
                }
            }

            if (!chunk.isEmpty()) {
                chunks.add(chunk);
                tokens += countPromptTokens(chunk, "system"); // 计算令牌数量
            }

            return new ChunkInfo(chunks, tokens);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    private static int countPromptTokens(String text, String type) {
        // 在这里实现你的令牌计数逻辑
        // 此函数根据指定的类型计算块中的令牌数量
        // 你应该替换此部分以实现实际的令牌计数逻辑
        return 0;
    }

    public static void main(String[] args) {
        String inputText = "这是一个示例文本。它包含多个句子。每个句子都不应被拆分。块的最大长度为30个字符或更少。运行应输出测试结果。";
        int maxChunkLength = 30; // 该值为每个分块的最大长度 应使用模型最大token长度*0.4 （fastGPT为0.45，并且单次生成25个问答对，但如果希望生成尽可能多的问答对，则可以保留更多的token给输出内容）

        ChunkInfo chunkInfo = splitTextIntoChunks(inputText, maxChunkLength);
        List<String> chunks = chunkInfo.getChunks();
        int tokens = chunkInfo.getTokens();

        System.out.println("总令牌数：" + tokens);
        for (int i = 0; i < chunks.size(); i++) {
            System.out.println("块 " + (i + 1) + "：");
            System.out.println(chunks.get(i));
            System.out.println();
        }
    }
}
