import * as SummaryTool from '@lyuboslavlyubenov/node-summary';
import * as Helper from '@lyuboslavlyubenov/node-summary/lib/helpers/html';

let contentEl = document.getElementById("content");

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    const title = Helper.getTitle(message);
    const content = Helper.convertHTMLToText(message);
    SummaryTool.summarize(title, content, function(err, summary) {
        if(err) console.log('Something went wrong man!');
        contentEl.innerHTML = summary;
    });
});

chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
    var currTab = tabs[0];
    if (currTab) {
        chrome.scripting.executeScript({
            target: { tabId: currTab.id },
            files: ['content.js']
        });
    }
  })
 
