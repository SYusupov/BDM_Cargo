package com.bdma.cargo.controller;

import com.bdma.cargo.model.UsersModel;
import org.apache.avro.reflect.ReflectData;
import org.apache.commons.net.ntp.TimeStamp;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.parquet.avro.AvroParquetWriter;
import org.apache.parquet.hadoop.ParquetFileWriter;
import org.apache.parquet.hadoop.ParquetWriter;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.io.IOException;
import java.util.UUID;

@RestController
@RequestMapping("/users")
public class UsersController {

    @Value("${output.directoryPath}")
    private String outputDirectoryPath;

    @Value("${output.filename.users}")
    private String outputFilename;

    @Value("${output.extension}")
    private String outputExtension;

    @PostMapping("/create")
    public ResponseEntity<Void> createUser(@RequestBody UsersModel creationRequest) {
        creationRequest.getAddress().setId(UUID.randomUUID().toString());
        creationRequest.setId(UUID.randomUUID().toString());
        long time = TimeStamp.getCurrentTime().getTime();
        Path dataFile = new Path(outputDirectoryPath + outputFilename + "-" + time + outputExtension);
        try (ParquetWriter<UsersModel> writer = AvroParquetWriter.<UsersModel>builder(dataFile)
                .withSchema(ReflectData.AllowNull.get().getSchema(UsersModel.class))
                .withDataModel(ReflectData.get())
                .withWriteMode(ParquetFileWriter.Mode.CREATE)
                .withConf(new Configuration())
                .build()) {
            writer.write(creationRequest);
        } catch (IOException e) {
            e.printStackTrace();
        }
        return ResponseEntity.ok().build();
    }
}
