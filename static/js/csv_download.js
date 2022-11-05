function saveData(csvStr, filename) {
    // string rep
    // var csvStr = "";
    // for (let r = 0; r < csvData.length; r++) {
    //     let row = csvData[r]
    //     for (let c = 0; c < row.length; c++) {
    //         let item = row[c]
    //         csvStr += item;
    //         if (c < row.length - 1)
    //             csvStr += ",";
    //     }
    //     if (r < csvStr.length - 1)
    //         csvStr += "\r\n";
    // }

    // define data blob
    var data = new Blob([csvStr]);

    // create & click temp link
    // slightly modded https://stackoverflow.com/a/15832662
    var link = document.createElement("a");
    link.download = filename;
    link.href = URL.createObjectURL(data);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    delete link;
}
