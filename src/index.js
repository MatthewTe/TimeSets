import fs from 'fs';

function ConvertCiteVisTextToJSON(filepath) {
    try {
        const data = fs.readFileSync(filepath, 'utf8')
        
        let processedCiteVDataset = []
        let articles = data.split("article")

        articles.forEach((article) => {

            let articleId = null
            let articleLines = article.split("\n")
            let authorFormatted = []
            let conceptsFormatted = []
            let affiliationsFormatted = []
            let indexTermFormatted = []
            let keywordFormatted = []
            let citations = []

            try {
                let selectedArticleId = articleLines[1]
                if (selectedArticleId.includes("infovis")) {
                    articleId = selectedArticleId
                } else {
                    console.log(`Could not find id index id string ${selectedArticleId}`)
                    console.log(articleLines)
                }

            } catch (error) {
                console.log("Cannot find the selected Article Id")
            }
            
            try {
                let authors = articleLines.filter((line) => line.startsWith('author'))
                authorFormatted = authors.map((authorString) => authorString.replace("author: ", ""))
            } catch (error) {
                console.log("Couldn't find any authors")
            }

            try {
                let concepts = articleLines.filter((line) => line.startsWith("concept: "))
                conceptsFormatted = concepts.map((conceptString) => conceptString.replace("concept: ", ""))
            } catch (error) {
                console.log("Couldn't find any concepts")
            }

            try {
                let affiliations = articleLines.filter((line) => line.startsWith("affiliation"))
                affiliationsFormatted = affiliations.map((affiliationString) => affiliationString.replace("affiliation: ", ""))
            }   catch (error) {
                console.log(`Couldn't find any affiliations`)
            }

            try {
                let indexTerms = articleLines.filter((line) => line.startsWith("indexterm: "))
                indexTermFormatted = indexTerms.map((indexTermsString) => indexTermsString.replace("indexterm: ", ""))
            } catch (error) {
                console.log("Couldn't find any index term values")
            }

            try {
                let keywords = articleLines.filter((line) => line.startsWith("keyword: "))
                keywordFormatted = keywords.map((line) => line.replace("keyword: ", ""))
            } catch (error) {
                console.log("Couldn't find any keywords")
            }

            try {
                let citationArrayIndex = articleLines.indexOf("citations:")
                let citationContent = articleLines.slice(citationArrayIndex, -1)
                citationContent.forEach((potentialCitation) => {
                    if (potentialCitation.includes('infovis')) {
                        citations.push(potentialCitation)
                    }
                })

            } catch (error) {
                console.log("Couldn't find the citation section")
            }

            let CiteVObject = {
                articleId: articleId,
                authors: authorFormatted,
                concepts: conceptsFormatted,
                affiliations: affiliationsFormatted,
                indexTerms: indexTermFormatted,
                keywords: keywordFormatted,
                citations: citations

            }

            if (articleId !== null) {
                processedCiteVDataset.push(CiteVObject)
            }
        })

        const processedDatasetStr = JSON.stringify(processedCiteVDataset)
        fs.writeFile("../data/infovis-citation-data.json", processedDatasetStr, function(err) {
            if (err) {
                console.log(`Error in saving the JSON data object to file ${err}`)
            }
        })


    } catch (error) {
        console.error(`Error in trying to read the file: ${error.messages}`)
    }
}

function loadConceptSets(filepath) {
    let rawData = fs.readFileSync(filepath, 'utf8')
    const data = JSON.parse(rawData)

    // Building set objects: 
    const sets = new Map()

    data.forEach((citation) => {

        let concepts = citation.concepts
        concepts.forEach((concept) => {
            if (sets.has(concept)) {
                sets.get(concept).push(citation.articleId)
            } else {
                sets.set(concept, [citation.articleId])
            }
        })
    })

    return sets
}

function createCitationMap(filepath) {
    let rawData = fs.readFileSync(filepath, 'utf8')
    const data = JSON.parse(rawData)

    // Building set objects: 
    const citations = new Map()

    data.forEach((citation) => {
        citations.set(
            citation.articleId, 
            {
                ...
                citation,
            }
        )       
    })

    return citations

}

// createCitationMap("/Users/matthewteelucksingh/Repos/TimeSets/data/infovis-citation-data.json")
// loadConceptSets("/Users/matthewteelucksingh/Repos/TimeSets/data/infovis-citation-data.json")