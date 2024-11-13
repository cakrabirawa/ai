import OpenAI from 'openai';
import { HttpsProxyAgent } from 'https-proxy-agent';

const proxyUrl = `http://10.12.30.8:8080`;
const proxyAgent = new HttpsProxyAgent(proxyUrl);

const openai = new OpenAI({
  apiKey: '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', // defaults to process.env["OPENAI_API_KEY"]
});

async function main() {
  const completion = await openai.completions.create({
    model: 'text-davinci-002',
    prompt: 'Say this is a test',
    max_tokens: 6,
    temperature: 0,    
  });

  console.log(completion.choices);
}
main().catch(console.error);