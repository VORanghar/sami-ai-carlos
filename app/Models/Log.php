<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Log extends Model
{
    protected $fillable = ['user_id', 'action', 'ip_address'];


    public function user()
    {
        return $this->hasOne(User::class, 'id', 'user_id');
    }
}
