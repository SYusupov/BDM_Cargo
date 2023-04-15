package com.bdma.cargo.controller;

import com.bdma.cargo.model.GasModel;
import org.apache.avro.reflect.ReflectData;
import org.apache.commons.net.ntp.TimeStamp;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.parquet.avro.AvroParquetWriter;
import org.apache.parquet.hadoop.ParquetFileWriter;
import org.apache.parquet.hadoop.ParquetWriter;
import org.json.JSONArray;
import org.json.JSONObject;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

@RestController
@RequestMapping("/gas")
public class GasController {

    @Value("${output.directoryPath}")
    private String outputDirectoryPath;

    @Value("${output.filename.gas}")
    private String outputFilename;

    @Value("${output.extension}")
    private String outputExtension;

    @GetMapping()
    public ResponseEntity<Void> getGasPrice() {
        long time = TimeStamp.getCurrentTime().getTime();
        Path dataFile = new Path(outputDirectoryPath + outputFilename + "-" + time + outputExtension);
        try (ParquetWriter<GasModel> writer = AvroParquetWriter.<GasModel>builder(dataFile)
                .withSchema(ReflectData.AllowNull.get().getSchema(GasModel.class))
                .withDataModel(ReflectData.get())
                .withWriteMode(ParquetFileWriter.Mode.CREATE)
                .withConf(new Configuration())
                .build()) {
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create("https://gas-price.p.rapidapi.com/europeanCountries"))
                    .header("X-RapidAPI-Key", "38bfcd91bdmsh5b9084a6d3f689dp1eeeeajsn4ee48dc54b02")
                    .header("X-RapidAPI-Host", "gas-price.p.rapidapi.com")
                    .method("GET", HttpRequest.BodyPublishers.noBody())
                    .build();
            HttpResponse<String> response = HttpClient.newHttpClient().send(request, HttpResponse.BodyHandlers.ofString());
            JSONObject jsonObject = new JSONObject(response.body());
            JSONArray gasObject = jsonObject.getJSONArray("results");
            for (int i = 0; i < gasObject.length(); i++) {
                JSONObject ss = gasObject.getJSONObject(i);
                writer.write(
                        new GasModel(ss.getString("currency"),
                                ss.getString("lpg"),
                                ss.getString("diesel"),
                                ss.getString("gasoline"),
                                ss.getString("country"))
                );
            }
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.badRequest().build();
        }
        return ResponseEntity.ok().build();
    }

}
