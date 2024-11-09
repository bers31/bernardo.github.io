<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('jadwal', function (Blueprint $table) {
            $table->string('id_jadwal')->primary();
            $table->string('kode_mk');
            $table->foreign('kode_mk')->references('kode_mk')->on('mata_kuliah')->onDelete('cascade');;
            $table->time('jam_mulai');
            $table->time('jam_selesai');
            $table->char('kode_kelas',1);
            $table->string('ruang');
            $table->foreign('ruang')->references('kode_ruang')->on('ruang')->onDelete('cascade');
            $table->enum('hari',['Senin','Selasa','Rabu','Kamis','Jumat','Sabtu','Minggu']);
            $table->unique(['hari','jam_mulai','ruang']);
            $table->integer('kuota');
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {   
        Schema::disableForeignKeyConstraints();
        Schema::dropIfExists('jadwal');
    }
};
