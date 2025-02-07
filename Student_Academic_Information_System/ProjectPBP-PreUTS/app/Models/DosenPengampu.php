<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class DosenPengampu extends Model
{
    //
    protected $table = 'dosen_pengampu';
    protected $primaryKey = ['nidn_dosen','id_jadwal'];
    public $incrementing = false;
    protected $fillable = ['nidn_dosen','id_jadwal'];

    protected function setKeysForSaveQuery($query)
    {
        $keys = $this->getKeyName();
        if(!is_array($keys)){
            return parent::setKeysForSaveQuery($query);
        }

        foreach($keys as $keyName){
            $query->where($keyName, '=', $this->getAttribute($keyName));
        }

        return $query;
    }

    public function dosen()
    {
        return $this->belongsTo(Dosen::class,  'nidn_dosen', 'nidn');
    }

    public function jadwal()
    {
        return $this->belongsTo(Jadwal::class, 'id_jadwal', 'id_jadwal');
    }
}
