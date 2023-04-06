// This is the code for a protobot app to obtain the source code from a PR and automatically ask for a code review using OpenAI API

const fs = require('fs');
const { Configuration, OpenAIApi } = require("openai");
const config =
    require('./config.js');
const configuration = new Configuration({
    organization: config.organization,
    apiKey: config.apiKey, 
});
const openai = new OpenAIApi(configuration);

module.exports = app => {
  app.on('pull_request.opened', async context => {
    const { data: pullRequest } = await context.octokit.pulls.get({
            owner: context.payload.repository.owner.login,
            repo: context.payload.repository.name,
            pull_number: context.payload.pull_request.number,
    });

const filesResponse = await context.octokit.pulls.listFiles({
     owner: context.payload.repository.owner.login,
     repo: context.payload.repository.name,
     pull_number: pullRequest.number
  });
  const files = filesResponse.data;

const req = `Review the following code from a pull request:\n${files.map(
    (file) => file.patch
  )}`;

const response = await openai.createCompletion({
      model: "text-davinci-003",
      prompt: req,
      max_tokens: 1024,
      temperature: 0.7,
      stop: null,
});

const comment = context.issue({
      body: response.data.choices[0].text,
});

await context.octokit.issues.createComment(comment);
  });
};
