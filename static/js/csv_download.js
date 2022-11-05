function saveCsv(csvStr) {
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
    window.open(URL.createObjectURL(data));
}
