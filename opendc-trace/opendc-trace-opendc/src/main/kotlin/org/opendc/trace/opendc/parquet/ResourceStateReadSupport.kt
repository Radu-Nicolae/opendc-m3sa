/*
 * Copyright (c) 2022 AtLarge Research
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

package org.opendc.trace.opendc.parquet

import org.apache.hadoop.conf.Configuration
import org.apache.parquet.hadoop.api.InitContext
import org.apache.parquet.hadoop.api.ReadSupport
import org.apache.parquet.io.api.RecordMaterializer
import org.apache.parquet.schema.*

/**
 * A [ReadSupport] instance for [ResourceState] objects.
 */
internal class ResourceStateReadSupport : ReadSupport<ResourceState>() {
    override fun init(context: InitContext): ReadContext {
        return ReadContext(READ_SCHEMA)
    }

    override fun prepareForRead(
        configuration: Configuration,
        keyValueMetaData: Map<String, String>,
        fileSchema: MessageType,
        readContext: ReadContext
    ): RecordMaterializer<ResourceState> = ResourceStateRecordMaterializer(readContext.requestedSchema)

    companion object {
        /**
         * Parquet read schema (version 2.0) for the "resource states" table in the trace.
         */
        @JvmStatic
        val READ_SCHEMA_V2_0: MessageType = Types.buildMessage()
            .addFields(
                Types
                    .required(PrimitiveType.PrimitiveTypeName.BINARY)
                    .`as`(LogicalTypeAnnotation.stringType())
                    .named("id"),
                Types
                    .required(PrimitiveType.PrimitiveTypeName.INT64)
                    .`as`(LogicalTypeAnnotation.timestampType(true, LogicalTypeAnnotation.TimeUnit.MILLIS))
                    .named("time"),
                Types
                    .required(PrimitiveType.PrimitiveTypeName.INT64)
                    .named("duration"),
                Types
                    .required(PrimitiveType.PrimitiveTypeName.INT32)
                    .named("cores"),
                Types
                    .required(PrimitiveType.PrimitiveTypeName.DOUBLE)
                    .named("cpuUsage")
            )
            .named("resource_state")

        /**
         * Parquet read schema (version 2.1) for the "resource states" table in the trace.
         */
        @JvmStatic
        val READ_SCHEMA_V2_1: MessageType = Types.buildMessage()
            .addFields(
                Types
                    .required(PrimitiveType.PrimitiveTypeName.BINARY)
                    .`as`(LogicalTypeAnnotation.stringType())
                    .named("id"),
                Types
                    .required(PrimitiveType.PrimitiveTypeName.INT64)
                    .`as`(LogicalTypeAnnotation.timestampType(true, LogicalTypeAnnotation.TimeUnit.MILLIS))
                    .named("timestamp"),
                Types
                    .required(PrimitiveType.PrimitiveTypeName.INT64)
                    .named("duration"),
                Types
                    .required(PrimitiveType.PrimitiveTypeName.INT32)
                    .named("cpu_count"),
                Types
                    .required(PrimitiveType.PrimitiveTypeName.DOUBLE)
                    .named("cpu_usage")
            )
            .named("resource_state")

        /**
         * Parquet read schema for the "resource states" table in the trace.
         */
        @JvmStatic
        val READ_SCHEMA: MessageType = READ_SCHEMA_V2_0.union(READ_SCHEMA_V2_1)
    }
}
